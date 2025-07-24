import{u as h,c as e,r as n,j as r,I as s,R as p,l as g,k as y,L as f}from"./index-dd8f6260.js";import{S as v}from"./index-44ee223b.js";import{v as I}from"./img1-71cf1da1.js";import{C as x}from"./Card-d6d2ad66.js";import{C as L}from"./CardBody-bb532dfb.js";import{U as b}from"./UncontrolledTooltip-508c0b57.js";function N(){const i=`Lorem Ipsum is simply dummy text of the printing and typesetting
  industry. Lorem Ipsum has been the industry's standard dummy
  text ever since the 1500s. Lorem Ipsum is simply dummy text of
  the printing and typesetting industry. Lorem Ipsum has been the
  industry's standard dummy text ever since the 1500s. ever since
  the 1500s. Lorem Ipsum is simply dummy text of the printing and
  typesetting industry. Lorem Ipsum has been the industry's
  standard dummy text ever since the 1500s. the printing and
  typesetting industry. Lorem Ipsum has been the industry's
  standard dummy text ever since the 1500s. ever since the 1500s.
  Lorem Ipsum is simply dummy text of the printing and typesetting
  industry. Lorem Ipsum has been the industry's standard dummy
  text ever since the 1500s.`,t=h(o=>o.layoutReducers),{userData:a}=t,d=[{Icon:s.Mail,title:"waleedrajputofficial@gmail.com",target:"profile-email"},{Icon:s.Phone,title:"03038724606",target:"profile-phone"},{Icon:s.Event,title:"Events",target:"profile-events"},{Icon:s.Setting,title:"Settings",target:"profile-settings"}];return e(n.Fragment,{children:e(x,{children:e(L,{children:r("div",{className:"user-profile",children:[r("div",{style:{marginBottom:"16px"},children:[e("div",{className:"user-img-container",children:e("img",{src:I,alt:""})}),e("h5",{className:"text-center text-primary mt-2 mb-0",children:a.username}),e("h6",{className:"text-center mt-0",children:"Admin"}),e("p",{className:"text-center",children:i.slice(0,300)}),e("p",{children:e("br",{})})]}),e("div",{className:"profile-icons-container",children:d.map((o,m)=>{const{Icon:l,title:u,target:c}=o;return r(n.Fragment,{children:[e(l,{size:20,id:`${c}-${m}`}),e(b,{target:`${c}-${m}`,children:e("small",{children:u})})]},m)})})]})})})})}function C(){return e(n.Fragment,{children:e(p,{className:"mt-3 match-height",children:e(v,{children:e(N,{})})})})}function k(){const i=g(),t=y(),{slug:a}=t.state?t.state:"";return console.log(t),r(n.Fragment,{children:[e(C,{}),e(f,{className:"w-25 m-2 ",onClick:()=>i(`/${a}/dashboard`),children:"Back"})]})}export{k as default};
