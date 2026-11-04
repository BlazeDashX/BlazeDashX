#!/usr/bin/env python3
"""Generate profile SVGs from GitHub's PUBLIC REST endpoints using GITHUB_TOKEN.

No extra secrets, third-party analytics endpoints or non-standard Python packages.
This is not a GitHub contribution-count calculator. Public Events API data
represents recent public activity, not all contributions or private work.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import html
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

USER = "BlazeDashX"
API_ROOT = "https://api.github.com"
BG, PANEL, INK, MUTED = "#0B111B", "#111C2A", "#F3F5F8", "#9AAFC4"
ORANGE, ORANGE_SOFT, BLUE = "#FF7B38", "#F4AF76", "#30C8F1"
GRID, LINE = "#1A2A3D", "#294158"
MONO = "'DejaVu Sans Mono', 'Consolas', monospace"
SANS = "'DejaVu Sans', Arial, sans-serif"


def esc(text):
    return html.escape(str(text if text is not None else ""), quote=True)


def cut(text, limit=55):
    txt = " ".join(str(text or "").split())
    return txt if len(txt) <= limit else txt[:limit - 1].rstrip() + "…"


def iso(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except (ValueError, AttributeError):
        return None


def fmt_date(value):
    t = iso(value) if isinstance(value, str) else value
    return t.strftime("%d %b %Y") if t else "Unknown"


def font(x, y, content, size=18, color=INK, weight=400, family=SANS, **extra):
    attrs = " ".join(f'{key.replace("_", "-")}="{esc(val)}"' for key,val in extra.items())
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" {attrs}>{esc(content)}</text>'


def rect(x,y,w,h,fill=PANEL,r=16,stroke=None,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"' + (f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '') + '/>'


def line(x1,y1,x2,y2,color=LINE,width=1,dash=None):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>'


def svg_shell(width,height,title,subtitle,stamp):
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
        '<defs><linearGradient id="wash" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0B111B"/><stop offset="1" stop-color="#101F31"/></linearGradient></defs>',
        rect(1,1,width-2,height-2,'url(#wash)',18,LINE,1),
        rect(24,25,3,24,ORANGE,1),
        font(44,45,title.upper(),13,BLUE,700,MONO,letter_spacing='2.4'),
        font(44,76,subtitle,16,MUTED),
        font(width-28,height-20,'PUBLIC GITHUB DATA  /  '+stamp,11,'#718AA0',400,MONO,text_anchor='end')]
    return out


def write_svg(path,elements):
    p=Path(path);p.parent.mkdir(parents=True, exist_ok=True)
    payload='\n'.join(elements+['</svg>'])
    p.write_text(payload,encoding='utf-8')
    return p


class Client:
    def __init__(self, token=None, fixture=None):
        self.token = token or ''
        self.fixture = fixture

    def get(self,path):
        if self.fixture is not None:
            if path in self.fixture:
                return self.fixture[path]
            raise KeyError('Fixture missing API response: '+path)
        headers={'Accept':'application/vnd.github+json',
                 'User-Agent':'BlazeDashX-Phoenix-AutoProfile',
                 'X-GitHub-Api-Version':'2022-11-28'}
        if self.token:
            headers['Authorization']='Bearer '+self.token
        req=urllib.request.Request(API_ROOT+path,headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            body=e.read().decode('utf-8','replace')
            raise RuntimeError(f'GitHub API {e.code} for {path}: {body[:250]}') from e
        except urllib.error.URLError as e:
            raise RuntimeError(f'Could not reach GitHub API at {path}: {e}') from e


def fetch_data(client):
    user=client.get(f'/users/{USER}')
    if not isinstance(user,dict) or user.get('login','').lower()!=USER.lower():
        raise ValueError('User API response did not match expected account')
    repos=[]
    for page in range(1,5):
        data=client.get(f'/users/{USER}/repos?type=owner&per_page=100&page={page}')
        if not isinstance(data,list): raise ValueError('Malformed repository listing')
        repos+=data
        if len(data)<100: break
    public_repos=[r for r in repos if not r.get('private') and not r.get('fork') and not r.get('archived') and r.get('name','').lower()!=USER.lower()]
    events=[]
    for page in range(1,4):
        arr=client.get(f'/users/{USER}/events/public?per_page=100&page={page}')
        if not isinstance(arr,list): raise ValueError('Malformed events listing')
        events+=arr
        if len(arr)<100: break
    return user,public_repos,events


def get_event_rows(events,now):
    valid=[]
    kinds={
      'PushEvent':'CODE PUSH','PullRequestEvent':'PULL REQUEST','IssuesEvent':'ISSUE',
      'ReleaseEvent':'RELEASE','CreateEvent':'NEW REF','ForkEvent':'FORK',
      'PullRequestReviewEvent':'CODE REVIEW','IssueCommentEvent':'DISCUSSION',
      'PublicEvent':'REPOSITORY', 'WatchEvent':'STARRED'
    }
    for event in events:
        t=iso(event.get('created_at'))
        if not t or t>now or (now-t).days>=31: continue
        typ=event.get('type','')
        if typ not in kinds: continue
        repo=(event.get('repo') or {}).get('name','')
        if repo.lower() == f'{USER}/{USER}'.lower(): continue
        payload=event.get('payload') or {}
        verb={
          'PushEvent':'Pushed code',
          'PullRequestEvent':f"{str(payload.get('action','Updated')).capitalize()} pull request",
          'IssuesEvent':f"{str(payload.get('action','Updated')).capitalize()} issue",
          'ReleaseEvent':'Published a release',
          'CreateEvent':f"Created {payload.get('ref_type','reference')}",
          'ForkEvent':'Forked repository',
          'PullRequestReviewEvent':'Reviewed pull request',
          'IssueCommentEvent':'Commented on issue',
          'PublicEvent':'Published repository',
          'WatchEvent':'Starred repository',
        }.get(typ,kinds[typ])
        # Never infer commit count or messages from PushEvent: GitHub public Events API may omit them.
        valid.append({'date':t,'kind':kinds[typ],'verb':verb,
                      'repo':repo.split('/')[-1] if repo else 'GitHub',
                      'full_repo':repo})
    return sorted(valid, key=lambda r:r['date'], reverse=True)


def panel_dashboard(output,user,repos,events,stamp,now):
    rows=get_event_rows(events,now)
    stars=sum(int(r.get('stargazers_count') or 0) for r in repos)
    last=max((iso(r.get('pushed_at')) for r in repos if iso(r.get('pushed_at'))),default=None)
    stats=[('PUBLIC REPOS',len(repos),'owned · non-fork · non-archived'),
           ('REPOSITORY STARS',stars,'public repositories'),
           ('FOLLOWERS',user.get('followers',0),'GitHub API'),
           ('RECENT EVENTS',len(rows),'public · last 30 days')]
    w,h=1200,280
    out=svg_shell(w,h,'System telemetry','Public account snapshot. Not a proficiency or contribution score.',stamp)
    for i,(label,val,hint) in enumerate(stats):
        x=24+i*294; y=104
        out.append(rect(x,y,282,126,PANEL,13,LINE))
        out.append(font(x+20,y+30,label,11,BLUE if i%2==0 else ORANGE_SOFT,700,MONO,letter_spacing='1.2'))
        out.append(font(x+18,y+82,f'{val:,}' if isinstance(val,int) else val,41,INK,700))
        out.append(font(x+20,y+107,hint,12,MUTED))
    if last:
        out.append(font(30,252,'LAST PUBLIC REPOSITORY PUSH  /  '+fmt_date(last),11,'#7F9AAF',400,MONO))
    write_svg(output,out)


def panel_activity(output,events,stamp,now):
    rows=get_event_rows(events,now)
    h=160+max(1,min(6,len(rows)))*64
    w=1200
    out=svg_shell(w,h,'Recent change log','A feed of public repository events from GitHub. The Events API covers recent activity.',stamp)
    rows=rows[:6]
    if rows:
        for i,ev in enumerate(rows):
            y=111+i*64
            out.append(line(30,y+58,1170,y+58,LINE))
            out.append(rect(31,y+10,108,32,'#20304A',7))
            out.append(font(85,y+31,ev['kind'][:12],10,BLUE,700,MONO,text_anchor='middle'))
            out.append(font(158,y+32,cut(ev['verb'],45),18,INK,600))
            out.append(font(158,y+52,cut(ev['repo'],72),13,MUTED))
            out.append(font(1168,y+30,fmt_date(ev['date']),13,ORANGE_SOFT,400,MONO,text_anchor='end'))
    else:
        out.append(font(40,145,'No public repository events were returned for the last 30 days.',20,INK,600))
        out.append(font(40,185,'This does not mean there were no private commits or other contributions.',14,MUTED))
    write_svg(output,out)


def panel_pulse(output,events,stamp,now):
    rows=get_event_rows(events,now)
    end=now.date()
    dates=[end-dt.timedelta(days=29-i) for i in range(30)]
    counts=collections.Counter(r['date'].date() for r in rows)
    values=[counts[d] for d in dates]
    top=max(values,default=0)
    w,h=1200,335
    out=svg_shell(w,h,'30-day event pulse','Daily public activity events; this is not the GitHub contribution calendar.',stamp)
    out.append(font(39,128,str(sum(values)),39,INK,700))
    out.append(font(39,153,'PUBLIC EVENTS',11,ORANGE_SOFT,700,MONO,letter_spacing='1.1'))
    startx=260; bottom=255; bw=22; gap=8; max_h=136
    out.append(line(startx-8,bottom,1180,bottom,'#3B4E64'))
    for i,n in enumerate(values):
        x=startx+i*(bw+gap)
        height=(n/top*max_h) if top else 2
        out.append(rect(x,bottom-max(2,round(height)),bw,max(2,round(height)),ORANGE if n==top and n else (BLUE if n else '#293A4F'),4))
        if i%7==0 or i==29:
            out.append(font(x+11,279,dates[i].strftime('%d %b'),10,MUTED,400,MONO,text_anchor='middle'))
    out.append(font(40,231,f'{sum(1 for v in values if v)} active days in public events',15,MUTED))
    out.append(font(40,271,'GitHub public event feed',12,'#7891A8'))
    write_svg(output,out)


def panel_languages(output,repos,stamp):
    counts=collections.Counter(r['language'] for r in repos if r.get('language'))
    items=counts.most_common(6)
    w,h=1200,130+max(1,len(items))*45
    out=svg_shell(w,h,'Language footprint','Primary language of each owned, non-fork public repository; not code volume.',stamp)
    top=max([n for _,n in items],default=1)
    if not items:
        out.append(font(40,160,'No primary-language information is available.',18,INK))
    for i,(name,n) in enumerate(items):
        y=113+i*45
        out.append(font(38,y+20,cut(name,30),16,INK,600))
        out.append(rect(270,y+4,760,20,'#1C2A3E',5))
        out.append(rect(270,y+4,760*n/top,20,ORANGE if i==0 else BLUE,5))
        out.append(font(1070,y+20,f'{n} repos',13,MUTED,600,MONO))
    write_svg(output,out)


def panel_radar(output,repos,stamp):
    repo_order=sorted(repos,key=lambda r:r.get('pushed_at') or '',reverse=True)[:4]
    w,h=1200,140+max(1,len(repo_order))*68
    out=svg_shell(w,h,'Repository radar','Most recently pushed public repositories; push dates are GitHub metadata.',stamp)
    if not repo_order: out.append(font(40,158,'No public repositories available.',17,MUTED))
    for i,r in enumerate(repo_order):
        y=111+i*68
        out.append(line(35,y+61,1164,y+61))
        out.append(font(45,y+19,f'{i+1:02}',11,ORANGE_SOFT,700,MONO))
        out.append(font(89,y+19,cut(r.get('name') or '?',47),19,INK,650))
        out.append(font(89,y+42,cut(r.get('description') or 'Public source repository',75),12,MUTED))
        out.append(font(870,y+20,cut(r.get('language') or 'Unclassified',18),12,BLUE,500,MONO,text_anchor='end'))
        out.append(font(1160,y+20,fmt_date(r.get('pushed_at')),12,ORANGE_SOFT,500,MONO,text_anchor='end'))
        out.append(font(1160,y+42,str(int(r.get('stargazers_count') or 0))+' stars',11,MUTED,400,MONO,text_anchor='end'))
    write_svg(output,out)




def display_repo_name(raw):
    """Readable labels for the portfolio map; metadata always uses true repository IDs."""
    display = {
        'personal-expense-tracker':'Expense Tracker',
        'a-05-emergency-hotline':'Emergency Hotline',
        'ayanco-frontend':'Ayanco',
        'learning_platform_frontend':'Learning Platform',
        'crown-clothing-nextjs':'Crown Clothing',
    }
    return display.get(str(raw or '').lower(), cut(raw,19))


def panel_constellation(output,repos,stamp):
    """Portfolio topology: live repo labels, illustrative positions, no invented dependencies."""
    ranked=sorted(repos,key=lambda r:r.get('pushed_at') or '',reverse=True)[:8]
    w,h=1200,480
    out=svg_shell(w,h,'Repository constellation','An original portfolio map: actual repos, illustrative layout. Node size follows public stars.',stamp)
    out += [
      '<defs><radialGradient id="hub"><stop offset="0" stop-color="#263F55"/><stop offset="1" stop-color="#0D1726"/></radialGradient></defs>',
      '<circle cx="600" cy="267" r="174" stroke="#2A455B" stroke-width="1" stroke-dasharray="4 9" fill="none"/>',
      '<circle cx="600" cy="267" r="112" stroke="#233C50" stroke-width="1" fill="none"/>',
      '<circle cx="600" cy="267" r="68" stroke="#2C7190" stroke-width="2" fill="url(#hub)"/>',
      '<path d="M564 280C580 251 597 258 606 235C615 246 621 259 640 268C624 270 616 287 604 308C596 289 578 287 564 280Z" fill="#FF7B38" opacity=".92"/>',
      '<path d="M592 281C604 262 611 254 616 246C626 265 621 281 610 297C605 289 601 284 592 281Z" fill="#30C8F1" opacity=".98"/>',
      font(600,335,'BLAZEDASHX',14,INK,700,MONO,text_anchor='middle'),
    ]
    positions=[(155,157),(425,133),(775,133),(1045,157),(1045,368),(775,392),(425,392),(155,368)]
    # Lines represent portfolio membership, never real repository dependencies.
    for i,r in enumerate(ranked):
        x,y=positions[i]
        color=ORANGE if i%3==0 else BLUE
        stars=int(r.get('stargazers_count') or 0)
        size=15+min(stars,12)*1.3
        out.append(f'<path d="M600 267 L{x} {y}" stroke="{color}" stroke-opacity=".24" stroke-width="1.5"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{size+11}" fill="none" stroke="{color}" stroke-opacity=".20" stroke-width="1.5"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{size}" fill="{BG}" stroke="{color}" stroke-width="2.3"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>')
        top=y<260
        name_y=y+size+24 if top else y-size-16
        lang_y=name_y+15 if top else name_y-18
        out.append(font(x,name_y,display_repo_name(r.get('name')),14,INK,650,SANS,text_anchor='middle'))
        out.append(font(x,lang_y,cut(r.get('language') or 'Unclassified',21),10,MUTED,400,MONO,text_anchor='middle'))
    out.append(font(34,452,f'{len(ranked)} recently pushed public repositories plotted  ·  constellation is a visual index, not an architecture graph',12,'#7B95AA'))
    write_svg(output,out)


def build(client,out,now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    if now.tzinfo is None: now=now.replace(tzinfo=dt.timezone.utc)
    user,repos,events=fetch_data(client)
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    stamp=now.strftime('%d %b %Y UTC').upper()
    panel_dashboard(out/'dashboard.svg',user,repos,events,stamp,now)
    panel_activity(out/'activity.svg',events,stamp,now)
    panel_pulse(out/'pulse.svg',events,stamp,now)
    panel_languages(out/'languages.svg',repos,stamp)
    panel_radar(out/'radar.svg',repos,stamp)
    panel_constellation(out/'constellation.svg',repos,stamp)
    # Store explanatory metadata, never sensitive tokens, for troubleshooting.
    (out/'updated.json').write_text(json.dumps({
       'source':'GitHub REST public endpoints',
       'user':USER,
       'generated_date_utc':now.date().isoformat(),
       'owned_public_repos_nonfork':len(repos),
       'recent_public_events_window_days':30,
       'recent_events_shown':len(get_event_rows(events,now)),
       'panels':['dashboard.svg','activity.svg','pulse.svg','languages.svg','radar.svg','constellation.svg']
    },indent=2)+'\n')
    return user,repos,events


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',default='assets/live')
    parser.add_argument('--fixture',help='Path to a JSON object keyed by API route, for offline tests/previews')
    parser.add_argument('--now',help='Fixed UTC ISO timestamp, for offline tests only')
    args=parser.parse_args()
    fixture=json.loads(Path(args.fixture).read_text()) if args.fixture else None
    now=iso(args.now) if args.now else None
    try:
        user,repos,events=build(Client(token=os.getenv('GITHUB_TOKEN'),fixture=fixture),args.out,now)
    except Exception as e:
        print(f'Generation failed without replacing existing visuals: {e}',file=sys.stderr)
        return 1
    print(f'Updated panels for {user["login"]} using {len(repos)} public owned non-fork repositories and {len(events)} retrieved public events.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
