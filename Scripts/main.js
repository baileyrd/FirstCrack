var body=document.body,timer;window.addEventListener('scroll',function(){clearTimeout(timer);if($("body").css("pointer-events")=="auto"){$("body").css("pointer-events","none")}timer=setTimeout(function(){$("body").css("pointer-events","auto")},500)},false);
function to_dark()
{
    $("body").css("background","333");
    $("body").css("color","#EFEFEF");
    $("a").css("color","#BFBFBF");
    $("a").mouseenter(function(){ $(this).css("color", "#FFF"); });
    $("a").mouseleave(function(){ $(this).css("color", "#BFBFBF"); });
}
function to_light()
{
    $("body").css("background","#F6F6F6");
    $("body").css("color","#000");
    $("a").css("color","#518341");
    $("a").mouseenter(function(){ $(this).css("color", "#C99199"); });
    $("a").mouseleave(function(){ $(this).css("color", "#518341"); });

    $(".linkpost").css("color","#8AC178");
    $(".linkpost").mouseenter(function(){ $(this).css("color", "#C97D88"); });
    $(".linkpost").mouseleave(function(){ $(this).css("color", "#8AC178"); });

    $(".original").css("color","#255515");
    $(".original").mouseenter(function(){ $(this).css("color", "#934953"); });
    $(".original").mouseleave(function(){ $(this).css("color", "#255515"); });
}
function CheckCookie()
{
    var expiration_date = new Date();
    expiration_date.setFullYear(expiration_date.getFullYear() + 1);
    if (document.cookie.match("mode=") == null)
    {
      document.cookie = "mode=light; expires="+expiration_date.toGMTString();
      to_light();
    }
    else if (document.cookie.match("mode=light") != null)
    {
        to_light();
    }
    else
    {
        to_dark();
    }
}
function ChangeCookie()
{
    var expiration_date = new Date();
    expiration_date.setFullYear(expiration_date.getFullYear() + 1);
    if (document.cookie.match("mode=light") != null)
    {
        document.cookie = "mode=dark; expires="+expiration_date.toGMTString();
        to_dark();
    }
    else
    {
        document.cookie = "mode=light; expires="+expiration_date.toGMTString();
        to_light();
    }
}

$(document).ready(function() {

    CheckCookie();

    document.onkeydown = checkKey;
    function checkKey(e)
    {
        e = e || window.event;
        if (e.keyCode == "68" && e.metaKey == false && e.shiftKey == false && e.altKey == false && e.altKey == false)
        {
            // alert(document.activeElement);
            ChangeCookie();
        }
    }
});