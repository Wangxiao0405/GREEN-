window.onload=function () {
    let btn=document.querySelector(".btn")
    let btn1=document.querySelector(".btn1")
    let aside=document.querySelector(".aside")
    // let asidelis=document.querySelectorAll(".aside .right a")
    console.log(aside,btn,btn1);
    btn.onclick=function () {
        aside.style.width="450px";
        btn.style.display="none";
    };
    btn1.onclick=function () {
        aside.style.width="0";
        btn.style.display="block";
    };

    //产品选项卡
    let pro_container=document.querySelector(".pro_container")
    let moves=document.querySelector(".pro_container .con");
    let rightbtn=document.querySelector(".arrows .right");
    let leftbtn=document.querySelector(".arrows .left");
    let width=parseInt(getComputedStyle(pro_container,null).width);
    console.log(pro_container,moves, rightbtn, leftbtn, width);
    rightbtn.onclick=function () {
        moves.style.transform="translateX("+(-width)+"px)"
    };
    leftbtn.onclick=function () {
        moves.style.transform="translateX(0px)"
    }
}