import{g as o,m as e,_ as t,ac as n,ah as r,d as a,i,r as l,bo as s,u as d,a as p,f as c,c as u,h as g,bp as v,a6 as m,ax as x,J as $}from"./index-CyT_JrVy.js";import{G as h,N as b,O as f,u as C,o as y,_ as w,w as P}from"./index-Cm96pFaw.js";const k=o=>{const{componentCls:e,popoverBg:r,popoverColor:a,width:i,fontWeightStrong:l,popoverPadding:s,boxShadowSecondary:d,colorTextHeading:p,borderRadiusLG:c,zIndexPopup:u,marginXS:g,colorBgElevated:v}=o;return[{[e]:t(t({},n(o)),{position:"absolute",top:0,left:{_skip_check_:!0,value:0},zIndex:u,fontWeight:"normal",whiteSpace:"normal",textAlign:"start",cursor:"auto",userSelect:"text","--antd-arrow-background-color":v,"&-rtl":{direction:"rtl"},"&-hidden":{display:"none"},[`${e}-content`]:{position:"relative"},[`${e}-inner`]:{backgroundColor:r,backgroundClip:"padding-box",borderRadius:c,boxShadow:d,padding:s},[`${e}-title`]:{minWidth:i,marginBottom:g,color:p,fontWeight:l},[`${e}-inner-content`]:{color:a}})},b(o,{colorBg:"var(--antd-arrow-background-color)"}),{[`${e}-pure`]:{position:"relative",maxWidth:"none",[`${e}-content`]:{display:"inline-block"}}}]},S=o=>{const{componentCls:e}=o;return{[e]:f.map((t=>{const n=o[`${t}-6`];return{[`&${e}-${t}`]:{"--antd-arrow-background-color":n,[`${e}-inner`]:{backgroundColor:n},[`${e}-arrow`]:{background:"transparent"}}}}))}},B=o=>{const{componentCls:e,lineWidth:t,lineType:n,colorSplit:r,paddingSM:a,controlHeight:i,fontSize:l,lineHeight:s,padding:d}=o,p=i-Math.round(l*s),c=p/2,u=p/2-t,g=d;return{[e]:{[`${e}-inner`]:{padding:0},[`${e}-title`]:{margin:0,padding:`${c}px ${g}px ${u}px`,borderBottom:`${t}px ${n} ${r}`},[`${e}-inner-content`]:{padding:`${a}px ${g}px`}}}},z=o("Popover",(o=>{const{colorBgElevated:t,colorText:n,wireframe:r}=o,a=e(o,{popoverBg:t,popoverColor:n,popoverPadding:12});return[k(a),S(a),r&&B(a),h(a,"zoom-big")]}),(o=>{let{zIndexPopupBase:e}=o;return{zIndexPopup:e+30,width:177}})),A=r(a({compatConfig:{MODE:3},name:"APopover",inheritAttrs:!1,props:i(t(t({},P()),{content:m(),title:m()}),t(t({},C()),{trigger:"hover",placement:"top",mouseEnterDelay:.1,mouseLeaveDelay:.1})),setup(o,e){let{expose:t,slots:n,attrs:r}=e;const a=l();s(void 0===o.visible),t({getPopupDomNode:()=>{var o,e;return null===(e=null===(o=a.value)||void 0===o?void 0:o.getPopupDomNode)||void 0===e?void 0:e.call(o)}});const{prefixCls:i,configProvider:m}=d("popover",o),[h,b]=z(i),f=p((()=>m.getPrefixCls())),C=()=>{var e,t;const{title:r=x(null===(e=n.title)||void 0===e?void 0:e.call(n)),content:a=x(null===(t=n.content)||void 0===t?void 0:t.call(n))}=o,l=!!(Array.isArray(r)?r.length:r),s=!!(Array.isArray(a)?a.length:r);return l||s?u($,null,[l&&u("div",{class:`${i.value}-title`},[r]),u("div",{class:`${i.value}-inner-content`},[a])]):null};return()=>{const e=c(o.overlayClassName,b.value);return h(u(w,g(g(g({},y(o,["title","content"])),r),{},{prefixCls:i.value,ref:a,overlayClassName:e,transitionName:v(f.value,"zoom-big",o.transitionName),"data-popover-inject":!0}),{title:C,default:n.default}))}}}));export{A as _};
