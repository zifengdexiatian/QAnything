import{a as Te,u as Z,p as me}from"./icon-loading-BT-1esjm.js";import{g as ie,u as ut}from"./index-BtipXdVs.js";import{d as G,A as c,B as d,C as o,J as f,G as s,L as ue,M as de,N as ee,r as I,c as u,R as k,z as F,E as L,W as S,H as B,F as J,D as be,X as T,a2 as X,a as dt,o as $e,b as ht,O as W,T as R,U as H,K as A,a3 as pt,S as ye,Q as _t,a4 as vt}from"./index-uS7D60Vj.js";import{u as Be,a as ft,b as gt,r as mt,C as yt}from"./utils-CXxq_1WL.js";import{u as bt,b as kt,_ as Ct,a as wt}from"./useChatSource-BnvcgUzt.js";import{u as St,a as Dt,b as Oe,D as At,f as It,h as qt,_ as xt,T as Lt}from"./html2canvas.esm-kffUbUtV.js";import{u as re,C as Tt,F as Ot,O as $t}from"./OptionList-DOrW3azC.js";import{_ as Bt,C as Ft}from"./ChatInfoPanel-BeNnHoZi.js";import{u as Et}from"./useChatSetting-DLMERjxB.js";import{B as Nt}from"./RightOutlined-dFqRQOx1.js";import"./collapseMotion-paX0PkVM.js";import"./index-vKtJiJDO.js";import"./index-BX6bNqE-.js";import"./injectionKey-DGYNie3Z.js";import"./slide-CIPjZ2vL.js";const Rt="/qanything/assets/icon-file-Bxz0aRpP.png",Ht=_=>(ue("data-v-ec2d7664"),_=_(),de(),_),Qt={class:"upload-box"},Ut=Ht(()=>o("img",{class:"icon-file",src:Rt,alt:"图标"},null,-1)),Mt={class:"title"},jt={class:"desc-content"},zt={class:"desc"},Kt={class:"desc"},Pt=G({__name:"UploadDom",props:{acceptList:{require:!0,type:Array,default:()=>[]}},emits:["update"],setup(_,{emit:h}){const p=ie().home,g=h,C=()=>{g("update")};return(r,y)=>(c(),d("div",Qt,[o("div",{class:"tips",onClick:C},[Ut,o("p",Mt,f(s(p).startDec),1),o("div",jt,[o("p",zt,f(s(p).updesc2),1),o("p",Kt,f(s(p).require1),1)])])]))}}),Vt=ee(Pt,[["__scopeId","data-v-ec2d7664"]]),Yt=_=>(ue("data-v-0587b9b1"),_=_(),de(),_),Jt={class:"default"},Xt={class:"box"},Wt={class:"title"},Zt=Yt(()=>o("span",null," ",-1)),Gt={class:"color"},es={class:"desc"},ts=G({__name:"Defaultpage",setup(_){const h=ie().home,{setFileList:p}=Te(),{setModalVisible:g}=Te(),{setCurrentId:C,getList:r,setCurrentKbName:y}=Z(),Q=[".doc",".docx",".ppt",".pptx",".xls",".xlsx",".pdf",".md",".jpg",".jpeg",".png",".bmp",".txt",".eml"],U=I(""),M=async()=>{console.log("updata");try{const i=await Be.createKb({kb_name:h.defaultName});+i.code==200&&(U.value=i.data.kb_id,C(i.data.kb_id),y(i.kb_name),g(!0),r())}catch(i){p([]),k.error(i.msg)}};return(i,te)=>(c(),d("div",Jt,[o("div",Xt,[o("p",Wt,[o("span",null,f(s(h).homeTitle1),1),Zt,o("span",Gt,f(s(h).homeTitle2),1)]),o("p",es,f(s(h).defaultDec),1),u(Vt,{"accept-list":Q,onUpdate:M})])]))}}),ss=ee(ts,[["__scopeId","data-v-0587b9b1"]]),os="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAAAARzQklUCAgICHwIZIgAAAEgSURBVFiF7ZaxDcJADEVt0lAyQkaAKzIHI0BxkmeKCxiFAaKDDRAdJQvkQpNIEeQu9gVoyK8SXZz/ZPssA8ya9e/KYofW2nVRFMuqqh4pP5fEL0IHRJQj4tl7f7XW7hLMd734tRqgrutV94yIBw1Ea37o3rMsC2YgWALn3N0Yc0PEbQuxNcbcnHMXjXnTNPuyLE9qgBbiooEYMmfmY8wjCqCBSDEXAUggUs0BAFDyUachoxYoyVwNMATRl9YcQFiCvl7LMcUcIDIHfiV1BkIlkM6Jt7gp5p9oQnEGQldNO6ySAMbu+RSIUQDpkEmFGNsHVBMuBSLYhESUe++vUvMR8A0zD0KI9gFtZzPzsbshAPF9ICoiymPbzLfjZ836Dz0BusANDR+zFvgAAAAASUVORK5CYII=",as=_=>(ue("data-v-b9aad642"),_=_(),de(),_),ns={class:"history-chat"},ls={class:"history-chat-content"},cs={class:"list"},rs=as(()=>o("div",{class:"line"},null,-1)),is=["onClick"],us=["onClick"],ds=G({__name:"HistoryChat",props:{observer:{type:Object,required:!0},observeDom:{type:Object,default:null},qaObserver:{type:Object,required:!0},qaObserveDom:{type:Object,default:null},showLoading:{type:Boolean,require:!0}},emits:["scrollBottom","setObserveDom","setQaObserverDom","clearHistory"],setup(_,{emit:h}){const p=_,{chatList:g,chatId:C,QA_List:r,qaPageId:y,pageId:Q,historyList:U}=F(re()),{deleteHistoryList:M,getChatById:i}=re(),{setSelectList:te}=Z(),x=h;function he(w){r.value.push({question:w,type:"user"})}function j(w,D,l,K,b,q){r.value.push({answer:l,question:w,itemInfo:D,type:"ai",qaId:b,copied:!1,like:!1,unlike:!1,source:q||[],showTools:!0,picList:K})}async function pe(w){if(!p.showLoading){C.value=w.historyId,r.value=[],y.value=1,te([...w.kbIds]),x("clearHistory");try{const D=i(C.value);p.qaObserveDom!==null&&(p.qaObserver.unobserve(p.qaObserveDom),x("setQaObserverDom",null)),D.list.forEach(l=>{l.type==="user"?he(l.question):l.type==="ai"&&j(l.question,l.itemInfo,l.answer,l.picList,l.qaId,l.source)}),x("scrollBottom"),D.list.length>=50&&await X(()=>{const l=document.getElementsByClassName("chat-li");l.length&&(p.qaObserver.observe(l[0]),x("setQaObserverDom",l[0]))})}catch(D){k.error(D.msg||"获取问答历史失败")}}}function z(){if(!p.showLoading){if(C.value===null){k.info("已切换最新对话");return}C.value=null,r.value=[],y.value=1,Q.value=1,x("clearHistory")}}async function _e(w,D){if(!p.showLoading)try{M(w.historyId),w.historyId===C.value&&z(),k.success("删除成功"),g.value.splice(D,1),await X(()=>{se()})}catch(l){k.error(l.msg||"删除失败")}}function se(){if(p.qaObserveDom!==null){p.qaObserver.unobserve(p.qaObserveDom),x("setQaObserverDom",null);const w=document.getElementsByClassName("chat-li");w.length&&(p.qaObserver.observe(w[0]),x("setQaObserverDom",w[0]))}}return(w,D)=>(c(),d("div",ns,[o("div",ls,[o("div",cs,[o("div",{class:L(["new-chat",[_.showLoading?"disabled":"",s(C)===null?"new-active":""]]),onClick:z},[u(S,{name:"new-chat"}),B(" "+f(s(ie)().home.newConversation),1)],2),(c(!0),d(J,null,be(s(U),(l,K)=>(c(),d("div",{key:l.historyId,class:L(["chat-item",s(C)===l.historyId?"item-active":"",_.showLoading?"disabled":""])},[rs,o("span",{onClick:b=>pe(l)},f(l.title),9,is),s(C)===l.historyId?(c(),d("img",{key:0,src:os,class:"close-icon",alt:"close",onClick:b=>_e(l,K)},null,8,us)):T("",!0)],2))),128))])])]))}}),hs=ee(ds,[["__scopeId","data-v-b9aad642"]]),Fe=_=>(ue("data-v-4bd46c43"),_=_(),de(),_),ps={class:"container showSider"},_s={class:"my-page"},vs={key:0,class:"user"},fs=Fe(()=>o("img",{class:"avatar",src:wt,alt:"头像"},null,-1)),gs={class:"question-text"},ms={key:1,class:"ai"},ys=Fe(()=>o("img",{class:"avatar",src:xt,alt:"头像"},null,-1)),bs={class:"ai-content"},ks={class:"ai-right"},Cs={key:1},ws={key:0},Ss={key:1},Ds={key:0},As={key:0},Is={key:1},qs={key:0},xs={class:"source-list"},Ls={class:"control"},Ts={class:"tips"},Os=["href"],$s=["onClick"],Bs={class:"source-content"},Fs=["innerHTML"],Es={class:"score"},Ns={class:"tips"},Rs={key:3,class:"feed-back"},Hs=["onClick"],Qs={class:"reload-text"},Us={class:"tools"},Ms={key:0,class:"stop-btn"},js={class:"question-box"},zs={class:"question"},Ks={class:"send-box"},Ps={class:"send-action"},Vs=G({__name:"Chat",setup(_){const h=ie().common,p=new Lt(e=>{e&&(r.value[r.value.length-1].answer+=e||"")}),{selectList:g,knowledgeBaseList:C}=F(Z()),{QA_List:r,chatId:y,pageId:Q,qaPageId:U,historyList:M}=F(re()),{chatSettingFormActive:i}=F(Et()),{copy:te}=St(),{addHistoryList:x,updateHistoryList:he,addChatList:j,clearChatList:pe}=re(),{setChatSourceVisible:z,setSourceType:_e,setSourceUrl:se,setTextContent:w}=bt(),{language:D}=F(ut()),l=I(""),K=dt(()=>{const e=i.value.context;if(e===0)return[];const t=r.value.filter(v=>v.type==="ai");return(e===11?t:t.slice(-e)).map(v=>[v.question,v.answer])}),b=I(!1),q=I([]),oe=I(null),ae=I(null);let O;const Ee=I(null),ke=I(null),$=()=>{X(()=>{var e;(e=ke.value)==null||e.scrollIntoView({behavior:"smooth",block:"end"})})},Ce=new IntersectionObserver(e=>{e.forEach(t=>{t.isIntersecting&&(console.log("entry.isIntersecting"),Q.value++)})}),we=new IntersectionObserver(e=>{e.forEach(t=>{t.isIntersecting&&(console.log("qa entry.isIntersecting"),U.value++)})});$e(()=>{$()}),ht(()=>{oe.value&&Ce.unobserve(oe.value),ae.value&&we.unobserve(ae.value)});const Ne=e=>{e.keyCode===13&&(e.altKey||e.ctrlKey||e.shiftKey||e.metaKey?l.value+=`
`:ve(),e.preventDefault())},Re=Dt((e,t)=>{if(e.like=!e.like,e.unlike=!1,_czc.push(["_trackEvent","qanything","问答页面","点赞","",""]),e.like){t.target.parentNode.style.animation="shake ease-in .5s";const n=setTimeout(()=>{clearTimeout(n),t.target.parentNode.style.animation=""},600)}},800),He=e=>{e.unlike=!e.unlike,e.like=!1,_czc.push(["_trackEvent","qanything","问答页面","点踩","",""])},Qe=e=>{te(e.answer).then(()=>{e.copied=!e.copied,k.success(h.copySuccess,1);const t=setTimeout(()=>{clearTimeout(t),e.copied=!e.copied},1e3)}).catch(()=>{k.error(h.copyFailed,1)})},Ue=e=>{r.value.push({question:e,type:"user"}),$()},Se=e=>{r.value.push({answer:"",question:e,onlySearch:i.value.capabilities.onlySearch,type:"ai",copied:!1,like:!1,unlike:!1,source:[],showTools:!1})},P=new yt,Me=e=>{oe.value=e},je=e=>{ae.value=e},De=(e,t,n)=>{try{he(e,t,n)}catch(v){k.error(v.msg||"更新对话失败")}};function ze(){if(!g.value.length)return;const e=[];g.value.forEach(t=>{C.value.some(n=>n.kb_id===t)&&e.push(t)}),g.value=e,M.value.forEach(t=>{y.value!==null&&t.historyId===y.value&&t.kbIds.join("")!==g.value.join("")&&De(t.title,t.historyId,g.value)})}const Ke=()=>{O&&O.abort(),p.done(),b.value=!1,r.value[r.value.length-1].showTools=!0},Pe=e=>{try{if(y.value!==null)return;e.length>100&&(e=e.substring(0,100)),y.value=x(e),De(e,y.value,g.value)}catch(t){k.error(t.msg||"创建对话失败")}},ve=()=>{if(!l.value.trim().length)return;if(b.value){k.warn("正在聊天中...请等待结束");return}if(!ot()){k.error("模型设置错误，请先检查模型配置");return}if(ze(),g.value.length)k.info({content:h.type==="zh"?`已选择 ${g.value.length} 个知识库进行问答`:` ${g.value.length} knowledge base has been selected`,icon:" "});else return k.warning(h.chooseError);const e=l.value;Pe(e),l.value="",Ue(e),j(y.value,r.value),b.value=!0,O=new AbortController,It(gt+"/local_doc_qa/local_doc_chat",{method:"POST",headers:{"Content-Type":"application/json",Accept:["text/event-stream","application/json"]},openWhenHidden:!0,body:JSON.stringify({user_id:ft,kb_ids:g.value,history:K.value,question:e,streaming:i.value.capabilities.onlySearch===!1,networking:i.value.capabilities.networkSearch,product_source:"saas",rerank:i.value.capabilities.rerank,only_need_search_results:i.value.capabilities.onlySearch,hybrid_search:i.value.capabilities.mixedSearch,max_token:i.value.maxToken,api_base:i.value.apiBase,api_key:i.value.apiKey,model:i.value.apiModelName,api_context_length:i.value.apiContextLength,chunk_size:i.value.chunkSize,top_p:i.value.top_P,temperature:i.value.temperature}),signal:O.signal,onopen(t){console.log("open",t),P.addChatSetting(i.value),t.ok&&t.headers.get("content-type")==="text/event-stream"?(Se(e),p.start()):t.headers.get("content-type")==="application/json"&&Se(e)},onmessage(t){var v;console.log("message",t);const n=JSON.parse(t.data);if((n==null?void 0:n.code)==200&&(n!=null&&n.response)&&n.msg==="success")p.add(n==null?void 0:n.response),$();else{const E=n.time_record.time_usage;delete E.retriever_search_by_milvus,P.addTime(n.time_record.time_usage),P.addToken(n.time_record.token_usage),P.addDate(Date.now())}(v=n==null?void 0:n.source_documents)!=null&&v.length&&(r.value[r.value.length-1].source=n==null?void 0:n.source_documents)},onclose(t){console.log("close",t),console.log(t),p.done(),O.abort(),b.value=!1,r.value[r.value.length-1].showTools=!0,r.value.at(-1).itemInfo=P.getChatInfo(),j(y.value,r.value),X(()=>{$()}),console.log(r.value)},onerror(t){throw console.log("error",t),p==null||p.done(),O==null||O.abort(),b.value=!1,r.value[r.value.length-1].showTools=!0,k.error(t.msg||"出错了"),j(y.value,r.value),X(()=>{$()}),t}})},Ve=e=>{console.log("reAnswer"),l.value=e.question,ve()},Ye=(e,t)=>{e.source[t].showDetailDataSource=!e.source[t].showDetailDataSource},Je=(e,t)=>{e.source[t].showDetailDataSource=!1},Xe=e=>{q.value.push(e)},We=e=>{q.value=q.value.filter(t=>t!==e)},{showModal:fe}=F(Oe()),ge=I(!1),ne=I(""),V=I(""),Ze=()=>{b.value||(V.value="download",fe.value=!0,ne.value=h.saveTip)},Ge=()=>{b.value||(V.value="delete",fe.value=!0,ne.value=h.clearTip)},et=async()=>{if(ge.value=!0,V.value==="download"){console.log("download");try{const e=document.getElementById("chat-ul"),n=(await qt(e,{useCORS:!0})).toDataURL("image/png"),v=document.createElement("a");v.style.display="none",v.href=n,v.setAttribute("download","chat-shot.png"),typeof v.download>"u"&&v.setAttribute("target","_blank"),document.body.appendChild(v),v.click(),document.body.removeChild(v),window.URL.revokeObjectURL(n),k.success("下载成功"),Promise.resolve()}catch(e){console.log(e),k.error(e.message||e.msg||"出错了")}}else V.value==="delete"&&(console.log("delete"),pe(y.value),y.value=null,r.value=[]);V.value="",ne.value="",ge.value=!1,fe.value=!1},{showSettingModal:tt}=F(Oe()),st=e=>{tt.value=e},ot=()=>!!(i.value.apiKey&&i.value.apiBase&&i.value.apiModelName);let Ae=["pdf","docx","xlsx","txt","jpg","png","jpeg"];const Ie=e=>{if(!e)return!1;const t=e.split(".");if(t.length){const n=t.pop();return!!Ae.includes(n)}else return!1},at=e=>{console.log("handleChatSource",e),Ie(e.file_name)&&nt(e)};async function nt(e){try{se(null);const t=await mt(await Be.getFile({file_id:e.file_id}));console.log("queryFile",t);const n=e.file_name.split(".").pop(),v=ct(n);if(console.log("b64Type",v),_e(n),se(`data:${v};base64,${t.base64_content}`),n==="txt"){const E=atob(t.base64_content),le=decodeURIComponent(escape(E));console.log("decodedTxt",le),w(le),z(!0)}else z(!0)}catch(t){k.error(t.msg||"获取文件失败")}}let lt=["application/pdf","application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet","text/plain","image/jpeg","image/png","image/jpeg"];function ct(e){const t=Ae.indexOf(e);return lt[t]}function rt(){console.log("清空")}return $(),(e,t)=>{const n=Nt,v=kt,E=Ct,le=Ot,it=vt;return c(),d(J,null,[u(hs,{observer:s(Ce),"observe-dom":s(oe),"qa-observe-dom":s(ae),"qa-observer":s(we),"show-loading":s(b),onScrollBottom:$,onSetObserveDom:Me,onSetQaObserverDom:je,onClearHistory:rt},null,8,["observer","observe-dom","qa-observe-dom","qa-observer","show-loading"]),o("div",ps,[o("div",_s,[o("div",{id:"chat",ref_key:"chatContainer",ref:Ee,class:"chat showSider"},[o("ul",{id:"chat-ul",ref_key:"scrollDom",ref:ke},[(c(!0),d(J,null,be(s(r),(a,N)=>{var qe,xe,Le;return c(),d("li",{key:N},[a.type==="user"?(c(),d("div",vs,[fs,o("p",gs,f(a.question),1)])):(c(),d("div",ms,[ys,o("div",bs,[o("div",ks,[a.onlySearch?a.onlySearch&&!a.source.length?(c(),d("p",{key:1,class:L(["question-text",[!a.source.length&&!((Le=a==null?void 0:a.picList)!=null&&Le.length)?"change-radius":"",a.showTools?"":"flashing"]])},[s(D)==="zh"?(c(),d("span",ws,"未找到信息来源")):(c(),d("span",Ss,"Information source not found"))],2)):T("",!0):(c(),d("p",{key:0,class:L(["question-text",[!a.source.length&&!((qe=a==null?void 0:a.picList)!=null&&qe.length)?"change-radius":"",a.showTools?"":"flashing"]])},[a.answer?(c(),W(Bt,{key:0,content:a.answer},null,8,["content"])):(c(),d("span",Cs,f(a.answer),1)),Object.keys(((xe=a==null?void 0:a.itemInfo)==null?void 0:xe.tokenInfo)||{}).length?(c(),W(Ft,{key:2,"chat-item-info":a.itemInfo},null,8,["chat-item-info"])):T("",!0)],2)),a.source.length?(c(),d(J,{key:2},[o("div",{class:L(["source-total",s(q).includes(N)?"":"source-total-last"])},[s(D)==="zh"?(c(),d("span",Ds,[a.onlySearch?(c(),d("span",As,"检索完成，")):T("",!0),B(" 找到了"+f(a.source.length)+"个信息来源： ",1)])):(c(),d("span",Is,[a.onlySearch?(c(),d("span",qs,"Search completed，")):T("",!0),B(" Found "+f(a.source.length)+" source of information ",1)])),R(u(S,{name:"down",onClick:m=>Xe(N)},null,8,["onClick"]),[[H,!s(q).includes(N)]]),R(u(S,{name:"up",onClick:m=>We(N)},null,8,["onClick"]),[[H,s(q).includes(N)]])],2),R(o("div",xs,[(c(!0),d(J,null,be(a.source,(m,ce)=>(c(),d("div",{key:ce,class:"data-source"},[R(o("p",Ls,[o("span",Ts,f(s(h).dataSource)+f(ce+1)+":",1),m.file_id.startsWith("http")?(c(),d("a",{key:0,href:m.file_id,target:"_blank"},f(m.file_name),9,Os)):(c(),d("span",{key:1,class:L(["file",Ie(m.file_name)?"filename-active":""]),onClick:Y=>at(m)},f(m.file_name),11,$s)),R(u(S,{name:"iconup",onClick:Y=>Je(a,ce)},null,8,["onClick"]),[[H,m.showDetailDataSource]]),R(u(S,{name:"icondown",onClick:Y=>Ye(a,ce)},null,8,["onClick"]),[[H,!m.showDetailDataSource]])],512),[[H,m.file_name]]),u(pt,{name:"sourceitem"},{default:A(()=>{var Y;return[R(o("div",Bs,[o("p",{innerHTML:(Y=m.content)==null?void 0:Y.replaceAll(`
`,"<br/>")},null,8,Fs),o("p",Es,[o("span",Ns,f(s(h).correlation),1),B(f(m.score),1)])],512),[[H,m.showDetailDataSource]])]}),_:2},1024)]))),128))],512),[[H,s(q).includes(N)]])],64)):T("",!0),a.showTools?(c(),d("div",Rs,[o("div",{class:"reload-box",onClick:m=>Ve(a)},[u(S,{name:"reload"}),o("span",Qs,f(s(h).regenerate),1)],8,Hs),o("div",Us,[u(S,{style:ye({color:a.copied?"#4D71FF":""}),name:"copy",onClick:m=>Qe(a)},null,8,["style","onClick"]),u(S,{style:ye({color:a.like?"#4D71FF":""}),name:"like",onClick:m=>s(Re)(a,m)},null,8,["style","onClick"]),u(S,{style:ye({color:a.unlike?"#4D71FF":""}),name:"unlike",onClick:m=>He(a)},null,8,["style","onClick"])])])):T("",!0)])])]))])}),128))],512)],512),s(b)?(c(),d("div",Ms,[u(n,{onClick:Ke},{icon:A(()=>[u(S,{name:"stop",class:L(s(b)?"loading":"")},null,8,["class"])]),default:A(()=>[B(" "+f(s(h).stop),1)]),_:1})])):T("",!0),o("div",js,[o("div",zs,[o("div",Ks,[u(v,{value:s(l),"onUpdate:value":t[0]||(t[0]=a=>_t(l)?l.value=a:null),class:"send-textarea","max-length":"200",bordered:!1,placeholder:s(h).problemPlaceholder,"auto-size":{minRows:4,maxRows:8},onKeydown:Ne},null,8,["value","placeholder"]),o("div",Ps,[u(E,{placement:"topLeft"},{content:A(()=>[B(f(s(h).chatToPic),1)]),default:A(()=>[o("span",{class:L(["download",s(b)?"isPreventClick":""]),onClick:Ze},[u(S,{name:"chat-download"})],2)]),_:1}),u(E,null,{content:A(()=>[B(f(s(h).clearChat),1)]),default:A(()=>[o("span",{class:L(["delete",s(b)?"isPreventClick":""]),onClick:Ge},[u(S,{name:"chat-delete"})],2)]),_:1}),u(E,null,{content:A(()=>[B(f(s(h).modelSettingTitle),1)]),default:A(()=>[o("span",{class:"setting",onClick:t[1]||(t[1]=a=>st(!0))},[u(S,{name:"chat-setting"})])]),_:1}),u(n,{type:"primary",disabled:s(b),shape:"circle",onClick:ve},{default:A(()=>[u(S,{name:"sendplane"})]),_:1},8,["disabled"])])])])])])]),u(Tt),u(At,{content:s(ne),"confirm-loading":s(ge),onOk:et},null,8,["content","confirm-loading"]),u(it,{theme:{token:{colorPrimary:"#5a47e5"}}},{default:A(()=>[u(le,{class:"scroll-btn",type:"primary",onClick:$},{icon:A(()=>[u(S,{name:"scroll"})]),_:1})]),_:1})],64)}}}),Ys=ee(Vs,[["__scopeId","data-v-4bd46c43"]]),Js={class:"page"},Xs={class:"container"},Ws=G({__name:"Home",setup(_){const{showDefault:h}=F(Z()),{setDefault:p,getList:g}=Z(),C=r=>{p(r),g()};return $e(()=>{g()}),(r,y)=>(c(),d("div",Js,[o("div",Xs,[s(h)===s(me).default?(c(),W(ss,{key:0,onChange:C})):s(h)===s(me).normal?(c(),W(Ys,{key:1})):s(h)===s(me).optionlist?(c(),W($t,{key:2})):T("",!0)])]))}}),_o=ee(Ws,[["__scopeId","data-v-a98d5469"]]);export{_o as default};