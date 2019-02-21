window.onload=function () {
    let btn=document.querySelector(".btn")
    let btn1=document.querySelector(".btn1")
    let aside=document.querySelector(".aside")
    console.log(aside,btn,btn1);
    btn.onclick=function () {
        aside.style.width="450px";
        btn.style.display="none";
    };
    btn1.onclick=function () {
        aside.style.width="0";
        btn.style.display="block";
    };
    //news页面选项卡
    let mainlis=document.querySelectorAll(".main .left li");
    let xxkBox=document.querySelectorAll(".xxkBox");
    console.log(mainlis, xxkBox);
    for (let i=0;i<mainlis.length;i++) {
        mainlis[i].onclick=function () {
            for (let j=0;j<mainlis.length;j++) {
                xxkBox[j].style.zIndex="5";
                mainlis[j].style.color="#666";
                mainlis[j].style.background="white";
            }
            xxkBox[i].style.zIndex="10";
            mainlis[i].style.color="white";
            mainlis[i].style.background="#89c92a"
        }
    }


}