Array.prototype.filter||(Array.prototype.filter=function(t,e){"use strict";if("Function"!=typeof t&&"function"!=typeof t||!this)throw new TypeError;var r=this.length>>>0,o=new Array(r),n=this,l=0,i=-1;if(void 0===e)for(;++i!==r;)i in this&&t(n[i],i,n)&&(o[l++]=n[i]);else for(;++i!==r;)i in this&&t.call(e,n[i],i,n)&&(o[l++]=n[i]);return o.length=l,o}),Array.prototype.forEach||(Array.prototype.forEach=function(t){var e,r;if(null==this)throw new TypeError('"this" is null or not defined');var o=Object(this),n=o.length>>>0;if("function"!=typeof t)throw new TypeError(t+" is not a function");for(arguments.length>1&&(e=arguments[1]),r=0;r<n;){var l;r in o&&(l=o[r],t.call(e,l,r,o)),r++}}),window.NodeList&&!NodeList.prototype.forEach&&(NodeList.prototype.forEach=Array.prototype.forEach),Array.prototype.indexOf||(Array.prototype.indexOf=function(t,e){var r;if(null==this)throw new TypeError('"this" is null or not defined');var o=Object(this),n=o.length>>>0;if(0===n)return-1;var l=0|e;if(l>=n)return-1;for(r=Math.max(l>=0?l:n-Math.abs(l),0);r<n;){if(r in o&&o[r]===t)return r;r++}return-1}),document.getElementsByClassName||(document.getElementsByClassName=function(t){var e,r,o,n=document,l=[];if(n.querySelectorAll)return n.querySelectorAll("."+t);if(n.evaluate)for(r=".//*[contains(concat(' ', @class, ' '), ' "+t+" ')]",e=n.evaluate(r,n,null,0,null);o=e.iterateNext();)l.push(o);else for(e=n.getElementsByTagName("*"),r=new RegExp("(^|\\s)"+t+"(\\s|$)"),o=0;o<e.length;o++)r.test(e[o].className)&&l.push(e[o]);return l}),document.querySelectorAll||(document.querySelectorAll=function(t){var e,r=document.createElement("style"),o=[];for(document.documentElement.firstChild.appendChild(r),document._qsa=[],r.styleSheet.cssText=t+"{x-qsa:expression(document._qsa && document._qsa.push(this))}",window.scrollBy(0,0),r.parentNode.removeChild(r);document._qsa.length;)(e=document._qsa.shift()).style.removeAttribute("x-qsa"),o.push(e);return document._qsa=null,o}),document.querySelector||(document.querySelector=function(t){var e=document.querySelectorAll(t);return e.length?e[0]:null}),Object.keys||(Object.keys=function(){"use strict";var t=Object.prototype.hasOwnProperty,e=!{toString:null}.propertyIsEnumerable("toString"),r=["toString","toLocaleString","valueOf","hasOwnProperty","isPrototypeOf","propertyIsEnumerable","constructor"],o=r.length;return function(n){if("function"!=typeof n&&("object"!=typeof n||null===n))throw new TypeError("Object.keys called on non-object");var l,i,s=[];for(l in n)t.call(n,l)&&s.push(l);if(e)for(i=0;i<o;i++)t.call(n,r[i])&&s.push(r[i]);return s}}()),"function"!=typeof String.prototype.trim&&(String.prototype.trim=function(){return this.replace(/^\s+|\s+$/g,"")}),String.prototype.replaceAll||(String.prototype.replaceAll=function(t,e){return"[object regexp]"===Object.prototype.toString.call(t).toLowerCase()?this.replace(t,e):this.replace(new RegExp(t,"g"),e)}),window.hasOwnProperty=window.hasOwnProperty||Object.prototype.hasOwnProperty;
if (typeof usi_commons === 'undefined') {
	usi_commons={logs:[],log:function(e){if(usi_commons.debug)try{usi_commons.logs.push(e),e instanceof Error?console.log(e.name+": "+e.message):console.log.apply(console,arguments)}catch(r){usi_commons.report_error_no_console(r)}},log_error:function(e){if(usi_commons.debug)try{e instanceof Error?console.log("%c USI Error:",usi_commons.log_styles.error,e.name+": "+e.message):console.log("%c USI Error:",usi_commons.log_styles.error,e)}catch(r){usi_commons.report_error_no_console(r)}},log_success:function(e){if(usi_commons.debug)try{console.log("%c USI Success:",usi_commons.log_styles.success,e)}catch(r){usi_commons.report_error_no_console(r)}},dir:function(e){if(usi_commons.debug)try{console.dir(e)}catch(r){usi_commons.report_error_no_console(r)}},log_styles:{error:"color: red; font-weight: bold;",success:"color: green; font-weight: bold;"},is_mobile:/iphone|ipod|ipad|android|blackberry|mobi/i.test(navigator.userAgent.toLowerCase()),device:/iphone|ipod|ipad|android|blackberry|mobi/i.test(navigator.userAgent.toLowerCase())?"mobile":"desktop",gup:function(e){try{e=e.replace(/[\[]/,"\\[").replace(/[\]]/,"\\]");var r="[\\?&]"+e+"=([^&#\\?]*)",t=RegExp(r).exec(window.location.href);if(null==t)return"";return t[1]}catch(i){usi_commons.report_error(i)}},load_script:function(e,r,t){try{0==e.indexOf("//")&&(e="https:"+e),(-1!=e.indexOf("/pixel.jsp")||-1!=e.indexOf("/blank.jsp")||-1!=e.indexOf("/customer_ip.jsp"))&&(e=e.replace(usi_commons.cdn,usi_commons.domain));var i=document.getElementsByTagName("head")[0],o=document.createElement("script");o.type="text/javascript";var n="";t||-1!=e.indexOf("/active/")||-1!=e.indexOf("_pixel.jsp")||-1!=e.indexOf("_throttle.jsp")||-1!=e.indexOf("metro")||-1!=e.indexOf("_suppress")||-1!=e.indexOf("product_recommendations")||-1!=e.indexOf("_pid.jsp")||-1!=e.indexOf("_zips")||(n=-1==e.indexOf("?")?"?":"&",-1!=e.indexOf("pv2.js")&&(n="%7C"),n+="si="+usi_commons.get_sess()),o.src=e+n,"function"==typeof r&&(o.onload=function(){try{r()}catch(e){usi_commons.report_error(e)}}),i.appendChild(o)}catch(s){usi_commons.report_error(s)}},fetch:function(e,r,t){try{t=t||{},0===e.indexOf("//")&&(e="https:"+e);var i=e.replace(usi_commons.cdn,usi_commons.domain),o="";if(-1!==i.indexOf("?")){var n=i.split("?");i=n[0],n.length>1&&(o=n[1])}var s={method:"POST",...t};return""!==o&&(s.body=new URLSearchParams(o)),fetch(i,s).then(e=>{if(!e.ok)throw Error(`HTTP error! status: `);return e.json()}).then(e=>{"function"==typeof r&&r(e)}).catch(e=>{usi_commons.report_error(e)})}catch(a){usi_commons.report_error(a)}},load_view:function(e,r,t,i){try{if("undefined"!=typeof usi_force||-1!=location.href.indexOf("usi_force")||null==usi_cookies.get("usi_sale")&&null==usi_cookies.get("usi_launched")&&null==usi_cookies.get("usi_launched"+r)){t=t||"";var o="";""!=usi_commons.gup("usi_force_date")?o="&usi_force_date="+usi_commons.gup("usi_force_date"):"undefined"!=typeof usi_cookies&&null!=usi_cookies.get("usi_force_date")&&(o="&usi_force_date="+usi_cookies.get("usi_force_date")),usi_commons.debug&&(o+="&usi_referrer="+encodeURIComponent(location.href)),0==t.indexOf("configID:")&&(o+="&configurationID="+encodeURIComponent(t.split("configID:")[1])),"undefined"!=typeof usi_cookies&&(null!=usi_cookies.get("usi_enable")&&(o+="&usi_enable=1"),null!=usi_cookies.get("usi_qa")&&(o+="&usi_qa=true"));var n=usi_commons.domain+"/view.jsp?hash="+e+"&siteID="+r+"&keys="+t+o;if(void 0!==usi_commons.last_view&&usi_commons.last_view==r+"_"+t)return;usi_commons.last_view=r+"_"+t,"undefined"!=typeof usi_js&&"function"==typeof usi_js.cleanup&&usi_js.cleanup(),usi_commons.load_script(n,i)}}catch(s){usi_commons.report_error(s)}},load_back_track:function(){try{if(usi_cookies.get("usi_back_clicked")){var e=usi_cookies.get("usi_back_clicked").split("_");if(3===e.length)return usi_commons.load_view(e[0],e[1],"configID:"+e[2]),!0}}catch(r){usi_commons.report_error(r)}return!1},remove_loads:function(){try{if(null!=document.getElementById("usi_obj")&&document.getElementById("usi_obj").parentNode.parentNode.removeChild(document.getElementById("usi_obj").parentNode),void 0!==usi_commons.usi_loads)for(var e in usi_commons.usi_loads)null!=document.getElementById("usi_"+e)&&document.getElementById("usi_"+e).parentNode.parentNode.removeChild(document.getElementById("usi_"+e).parentNode)}catch(r){usi_commons.report_error(r)}},load:function(e,r,t,i){try{if(void 0!==window["usi_"+r])return!1;t=t||"";var o="";""!=usi_commons.gup("usi_force_date")?o="&usi_force_date="+usi_commons.gup("usi_force_date"):"undefined"!=typeof usi_cookies&&null!=usi_cookies.get("usi_force_date")&&(o="&usi_force_date="+usi_cookies.get("usi_force_date")),usi_commons.debug&&(o+="&usi_referrer="+encodeURIComponent(location.href)),"undefined"!=typeof usi_cookies&&(null!=usi_cookies.get("usi_enable")&&(o+="&usi_enable=1"),null!=usi_cookies.get("usi_qa")&&(o+="&usi_qa=true"));var n=usi_commons.domain+"/usi_load.jsp?hash="+e+"&siteID="+r+"&keys="+t+o;usi_commons.load_script(n,i),void 0===usi_commons.usi_loads&&(usi_commons.usi_loads={}),usi_commons.usi_loads[r]=r}catch(s){usi_commons.report_error(s)}},load_precapture:function(e,r,t){try{if(void 0!==usi_commons.last_precapture_siteID&&usi_commons.last_precapture_siteID==r)return;usi_commons.last_precapture_siteID=r;var i="";"undefined"!=typeof usi_cookies&&null!=usi_cookies.get("usi_enable")&&(i+="&usi_enable=1");var o=usi_commons.domain+"/hound/monitor.jsp?qs="+e+"&siteID="+r+i;usi_commons.load_script(o,t)}catch(n){usi_commons.report_error(n)}},load_mail:function(e,r,t){try{var i=usi_commons.domain+"/mail.jsp?qs="+e+"&siteID="+r+"&domain="+encodeURIComponent(usi_commons.domain);usi_commons.load_script(i,t)}catch(o){usi_commons.report_error(o)}},load_products:function(e){try{if(!e.siteID||!e.pid)return;var r="";["siteID","association_siteID","pid","less_expensive","rows","days_back","force_exact","match","nomatch","name_from","image_from","price_from","url_from","extra_from","extra_merge","custom_callback","allow_dupe_names","expire_seconds","name","ordersID","cartsID","viewsID","companyID","order_by"].forEach(function(t,i){e[t]&&(r+=(0==i?"?":"&")+t+"="+e[t])}),e.filters&&(r+="&filters="+encodeURIComponent(e.filters.map(function(e){return encodeURIComponent(e)}).join("&"))),usi_commons.load_script(usi_commons.cdn+"/utility/product_recommendations_filter_v3.jsp"+r,function(){if("function"==typeof e.callback){var r="string"==typeof e.name?e.name.replace("usi_app."):"product_rec";e.callback("object"==typeof usi_app&&usi_app[r]?usi_app[r]:{})}})}catch(t){usi_commons.report_error(t)}},send_prod_rec:function(e,r,t){var i=!1;try{if(document.getElementsByTagName("html").length>0&&null!=document.getElementsByTagName("html")[0].className&&-1!=document.getElementsByTagName("html")[0].className.indexOf("translated"))return!1;var o=[e,r.name,r.link,r.pid,r.price,r.image];if(-1==o.indexOf(void 0)){var n=[e,r.name.replace(/\|/g,"&#124;"),r.link,r.pid,r.price,r.image].join("|")+"|";r.extra&&(n+=r.extra.replace(/\|/g,"&#124;")+"|"),usi_commons.load_script(usi_commons.domain+"/utility/pv2."+(t?"jsp":"js")+"?"+encodeURIComponent(n)),i=!0}}catch(s){usi_commons.report_error(s),i=!1}return i},report_error:function(e){if(null!=e&&("string"==typeof e&&(e=Error(e)),e instanceof Error)){if(void 0===usi_commons.error_reported){if(usi_commons.error_reported=!0,-1!==location.href.indexOf("usishowerrors"))throw e;usi_commons.load_script(usi_commons.domain+"/err.jsp?oops="+encodeURIComponent(e.message)+"-"+encodeURIComponent(e.stack)+"&url="+encodeURIComponent(location.href)),usi_commons.log_error(e.message),usi_commons.dir(e)}}},report_error_no_console:function(e){if(null!=e&&("string"==typeof e&&(e=Error(e)),e instanceof Error)){if(void 0===usi_commons.error_reported){if(usi_commons.error_reported=!0,-1!==location.href.indexOf("usishowerrors"))throw e;usi_commons.load_script(usi_commons.domain+"/err.jsp?oops="+encodeURIComponent(e.message)+"-"+encodeURIComponent(e.stack)+"&url="+encodeURIComponent(location.href))}}},gup_or_get_cookie:function(e,r,t){try{if("undefined"==typeof usi_cookies){usi_commons.log_error("usi_cookies is not defined");return}r=r||usi_cookies.expire_time.day,"usi_enable"==e&&(r=usi_cookies.expire_time.hour);var i=null,o=usi_commons.gup(e);return""!==o?(i=o,usi_cookies.set(e,i,r,t)):i=usi_cookies.get(e),i||""}catch(n){usi_commons.report_error(n)}},get_sess:function(){var e=null;if("undefined"==typeof usi_cookies)return"";try{if(null==usi_cookies.get("usi_si")){var r=Math.random().toString(36).substring(2);return r.length>6&&(r=r.substring(0,6)),e=r+"_"+Math.round(new Date().getTime()/1e3),usi_cookies.set("usi_si",e,86400),e}null!=usi_cookies.get("usi_si")&&(e=usi_cookies.get("usi_si")),usi_cookies.set("usi_si",e,86400)}catch(t){usi_commons.report_error(t)}return e},get_id:function(e){e||(e="");var r=null;try{if(null==usi_cookies.get("usi_v")&&null==usi_cookies.get("usi_id"+e)){var t=Math.random().toString(36).substring(2);return t.length>6&&(t=t.substring(0,6)),r=t+"_"+Math.round(new Date().getTime()/1e3),usi_cookies.set("usi_id"+e,r,2592e3,!0),r}null!=usi_cookies.get("usi_v")&&(r=usi_cookies.get("usi_v")),null!=usi_cookies.get("usi_id"+e)&&(r=usi_cookies.get("usi_id"+e)),usi_cookies.set("usi_id"+e,r,2592e3,!0)}catch(i){usi_commons.report_error(i)}return r},load_session_data:function(e){try{null==usi_cookies.get_json("usi_session_data")?usi_commons.load_script(usi_commons.domain+"/utility/session_data.jsp?extended="+(e?"true":"false")):(usi_app.session_data=usi_cookies.get_json("usi_session_data"),void 0!==usi_app.session_data_callback&&usi_app.session_data_callback())}catch(r){usi_commons.report_error(r)}},customer_ip:function(e){try{-1!=e?usi_cookies.set("usi_suppress","1",usi_cookies.expire_time.never):usi_app.main()}catch(r){usi_commons.report_error(r)}},customer_check:function(e){try{if(!usi_app.is_enabled&&!usi_cookies.value_exists("usi_ip_checked"))return usi_cookies.set("usi_ip_checked","1",usi_cookies.expire_time.day),usi_commons.load_script(usi_commons.domain+"/utility/customer_ip2.jsp?companyID="+e),!1;return!0}catch(r){usi_commons.report_error(r)}}};
	usi_commons.domain = "https://app.upsellit.com";
	usi_commons.cdn = "https://www.upsellit.com";
	usi_commons.debug = false;
	if (location.href.indexOf("usidebug") != -1 || location.href.indexOf("usi_debug") != -1) {
		usi_commons.debug = true;
	}
	setTimeout(function() {
		try {
			if (usi_commons.gup_or_get_cookie("usi_debug") != "") usi_commons.debug = true;
			if (usi_commons.gup_or_get_cookie("usi_qa") != "") {
				usi_commons.domain = usi_commons.cdn = "https://prod.upsellit.com";
			}
		} catch(err) {
			usi_commons.report_error(err);
		}
	}, 1000);
}

if (typeof usi_app === 'undefined') {
	try {
		if("undefined"==typeof usi_cookies){if(usi_cookies={expire_time:{minute:60,hour:3600,two_hours:7200,four_hours:14400,day:86400,week:604800,two_weeks:1209600,month:2592e3,year:31536e3,never:31536e4},max_cookies_count:15,max_cookie_length:1e3,update_window_name:function(e,r,t){try{var i=-1;if(-1!=t){var o=new Date;o.setTime(o.getTime()+1e3*t),i=o.getTime()}var n=window.top||window,a=0;null!=r&&-1!=r.indexOf("=")&&(r=r.replace(RegExp("=","g"),"USIEQLS")),null!=r&&-1!=r.indexOf(";")&&(r=r.replace(RegExp(";","g"),"USIPRNS"));for(var c=n.name.split(";"),u="",l=0;l<c.length;l++){var s=c[l].split("=");3==s.length?(s[0]==e&&(s[1]=r,s[2]=i,a=1),null!=s[1]&&"null"!=s[1]&&(u+=s[0]+"="+s[1]+"="+s[2]+";")):""!=c[l]&&(u+=c[l]+";")}0==a&&(u+=e+"="+r+"="+i+";"),n.name=u}catch(f){}},flush_window_name:function(e){try{for(var r=window.top||window,t=r.name.split(";"),i="",o=0;o<t.length;o++){var n=t[o].split("=");3==n.length&&(0==n[0].indexOf(e)||(i+=t[o]+";"))}r.name=i}catch(a){}},get_from_window_name:function(e){try{for(var r,t,i=(window.top||window).name.split(";"),o=0;o<i.length;o++){var n=i[o].split("=");if(3==n.length){if(n[0]==e&&(t=n[1],-1!=t.indexOf("USIEQLS")&&(t=t.replace(/USIEQLS/g,"=")),-1!=t.indexOf("USIPRNS")&&(t=t.replace(/USIPRNS/g,";")),!("-1"!=n[2]&&0>usi_cookies.datediff(n[2]))))return r=[t,n[2]]}else if(2==n.length&&n[0]==e)return t=n[1],-1!=t.indexOf("USIEQLS")&&(t=t.replace(/USIEQLS/g,"=")),-1!=t.indexOf("USIPRNS")&&(t=t.replace(/USIPRNS/g,";")),r=[t,new Date().getTime()+6048e5]}}catch(a){}return null},datediff:function(e){return e-new Date().getTime()},count_cookies:function(e){return e=e||"usi_",usi_cookies.search_cookies(e).length},root_domain:function(){try{var e=document.domain.split("."),r=e[e.length-1];if("com"==r||"net"==r||"org"==r||"us"==r||"co"==r||"ca"==r)return e[e.length-2]+"."+e[e.length-1]}catch(t){}return 0==document.domain.indexOf("www.")?document.domain.replace("www.",""):document.domain},create_cookie:function(e,r,t){if(!1!==navigator.cookieEnabled&&void 0===window.usi_nocookies){var i="";if(-1!=t){var o=new Date;o.setTime(o.getTime()+1e3*t),i="; expires="+o.toGMTString()}var n="samesite=none;";0==location.href.indexOf("https://")&&(n+="secure;");var a=usi_cookies.root_domain();"undefined"!=typeof usi_parent_domain&&-1!=document.domain.indexOf(usi_parent_domain)&&(a=usi_parent_domain),document.cookie=e+"="+encodeURIComponent(r)+i+"; path=/;domain="+a+"; "+n}},create_nonencoded_cookie:function(e,r,t,i){if(!1!==navigator.cookieEnabled&&void 0===window.usi_nocookies){var o="";if(-1!=t){var n=new Date;n.setTime(n.getTime()+1e3*t),o="; expires="+n.toGMTString()}var a="samesite=none;";0==location.href.indexOf("https://")&&(a+="secure;");var c=usi_cookies.root_domain();document.cookie=e+"="+r+o+"; path=/;domain="+c+"; "+a,i||(document.cookie=e+"="+r+o+"; path=/;domain="+location.host+"; "+a,document.cookie=e+"="+r+o+"; path=/;domain=; "+a)}},read_cookie:function(e){if(!1===navigator.cookieEnabled)return null;var r=e+"=",t=[];try{t=document.cookie.split(";")}catch(i){}for(var o=0;o<t.length;o++){for(var n=t[o];" "==n.charAt(0);)n=n.substring(1,n.length);if(0==n.indexOf(r))return decodeURIComponent(n.substring(r.length,n.length))}return null},del:function(e){usi_cookies.set(e,null,-100);try{null!=localStorage&&localStorage.removeItem(e),null!=sessionStorage&&sessionStorage.removeItem(e)}catch(r){}},get_ls:function(e){try{var r=localStorage.getItem(e);if(null!=r){if(0==r.indexOf("{")&&-1!=r.indexOf("usi_expires")){var t=JSON.parse(r);if(new Date().getTime()>t.usi_expires)return localStorage.removeItem(e),null;r=t.value}return decodeURIComponent(r)}}catch(i){}return null},get:function(e){var r=usi_cookies.read_cookie(e);if(null!=r)return r;try{if(null!=localStorage&&(r=usi_cookies.get_ls(e),null!=r))return r;if(null!=sessionStorage&&(r=sessionStorage.getItem(e),void 0===r&&(r=null),null!=r))return decodeURIComponent(r)}catch(t){}var i=usi_cookies.get_from_window_name(e);if(null!=i&&i.length>1)try{r=decodeURIComponent(i[0])}catch(o){return i[0]}return r},get_json:function(e){var r=null,t=usi_cookies.get(e);if(null==t)return null;try{r=JSON.parse(t)}catch(i){t=t.replace(/\\"/g,'"');try{r=JSON.parse(JSON.parse(t))}catch(o){try{r=JSON.parse(t)}catch(n){}}}return r},search_cookies:function(e){e=e||"";var r=[];return document.cookie.split(";").forEach(function(t){var i=t.split("=")[0].trim();(""===e||0===i.indexOf(e))&&r.push(i)}),r},set:function(e,r,t,i){"undefined"!=typeof usi_nevercookie&&!0==usi_nevercookie&&(i=!1),void 0===t&&(t=-1);try{r=r.replace(/(\r\n|\n|\r)/gm,"")}catch(o){}"undefined"==typeof usi_windownameless&&(null==r||r.length<1e3)&&usi_cookies.update_window_name(e+"",r+"",t);try{if(t>0&&null!=localStorage){var n=new Date,a={value:r,usi_expires:n.getTime()+1e3*t};localStorage.setItem(e,JSON.stringify(a))}else null!=sessionStorage&&sessionStorage.setItem(e,r)}catch(c){}if(i||null==r){if(null!=r){if(null==usi_cookies.read_cookie(e)&&!i&&usi_cookies.search_cookies("usi_").length+1>usi_cookies.max_cookies_count){usi_cookies.report_error('Set cookie "'+e+'" failed. Max cookies count is '+usi_cookies.max_cookies_count);return}if(r.length>usi_cookies.max_cookie_length){usi_cookies.report_error('Cookie "'+e+'" truncated ('+r.length+"). Max single-cookie length is "+usi_cookies.max_cookie_length);return}}usi_cookies.create_cookie(e,r,t)}},set_json:function(e,r,t,i){var o=JSON.stringify(r).replace(/^"/,"").replace(/"$/,"");usi_cookies.set(e,o,t,i)},flush:function(e){e=e||"usi_";var r,t,i,o=document.cookie.split(";");for(r=0;r<o.length;r++)0==(t=o[r]).trim().toLowerCase().indexOf(e)&&(i=t.trim().split("=")[0],usi_cookies.del(i));usi_cookies.flush_window_name(e);try{if(null!=localStorage)for(var n in localStorage)0==n.indexOf(e)&&localStorage.removeItem(n);if(null!=sessionStorage)for(var n in sessionStorage)0==n.indexOf(e)&&sessionStorage.removeItem(n)}catch(a){}},print:function(){for(var e=document.cookie.split(";"),r="",t="",i=0;i<e.length;i++){var o=e[i];0==o.trim().toLowerCase().indexOf("usi_")&&(console.log(decodeURIComponent(o.trim())+" (cookie)"),t+=decodeURIComponent(o.trim())+" (cookie), ",r+=","+o.trim().toLowerCase().split("=")[0]+",")}try{if(null!=localStorage)for(var n in localStorage)0==n.indexOf("usi_")&&"string"==typeof localStorage[n]&&-1==r.indexOf(","+n+",")&&(console.log(n+"="+usi_cookies.get_ls(n)+" (localStorage)"),t+=n+"="+usi_cookies.get_ls(n)+" (localStorage), ",r+=","+n+",");if(null!=sessionStorage)for(var n in sessionStorage)0==n.indexOf("usi_")&&"string"==typeof sessionStorage[n]&&-1==r.indexOf(","+n+",")&&(console.log(n+"="+sessionStorage[n]+" (sessionStorage)"),t+=n+"="+sessionStorage[n]+" (sessionStorage), ",r+=","+n+",")}catch(a){}for(var c=(window.top||window).name.split(";"),u=0;u<c.length;u++){var l=c[u].split("=");if(3==l.length&&0==l[0].indexOf("usi_")&&-1==r.indexOf(","+l[0]+",")){var s=l[1];-1!=s.indexOf("USIEQLS")&&(s=s.replace(/USIEQLS/g,"=")),-1!=s.indexOf("USIPRNS")&&(s=s.replace(/USIPRNS/g,";")),console.log(l[0]+"="+s+" (window.name)"),t+=l[0]+"="+s+" (window.name), ",r+=","+o.trim().toLowerCase().split("=")[0]+","}}return t},value_exists:function(){var e,r;for(e=0;e<arguments.length;e++)if(r=usi_cookies.get(arguments[e]),""===r||null===r||"null"===r||"undefined"===r)return!1;return!0},report_error:function(e){"undefined"!=typeof usi_commons&&"function"==typeof usi_commons.report_error&&usi_commons.report_error(e)},check_multi_domain:function(){try{"undefined"!=typeof usi_app&&usi_app.company_id?usi_cookies.get("usi_app.company_id")?usi_cookies.get("usi_app.company_id")!==usi_app.company_id&&(window.name=""):usi_cookies.set("usi_app.company_id",usi_app.company_id):setTimeout(function(){usi_cookies.check_multi_domain()},2e3)}catch(e){"undefined"!=typeof usi_commons&&usi_commons.report_error(e)}},monitor_page_views:function(){try{if(void 0===usi_cookies.last_url||usi_cookies.last_url!=location.href){usi_cookies.last_url=location.href;var e=window.self===window.top,r=-1!==location.href.indexOf("/checkouts/");e&&(usi_cookies.get("usi_entry_url_1")||usi_cookies.set("usi_entry_url_1",usi_cookies.last_url,21600),null==document.referrer||usi_cookies.get("usi_referrer_url")||-1!=document.referrer.indexOf(location.host)||usi_cookies.set("usi_referrer_url",document.referrer||"direct traffic",21600)),(e||r)&&(usi_cookies.get("usi_entry_url_1")&&usi_cookies.get("usi_entry_url_1")!=usi_cookies.last_url&&usi_cookies.set("usi_last_url_1",usi_cookies.last_url,21600),usi_cookies.set("usi_pv_count",String(Number(usi_cookies.get("usi_pv_count")||0)+1),21600))}setTimeout(usi_cookies.monitor_page_views,2e3)}catch(t){"undefined"!=typeof usi_commons&&usi_commons.report_error(t)}}},"undefined"!=typeof usi_commons&&"function"==typeof usi_commons.gup&&"function"==typeof usi_commons.gup_or_get_cookie)try{usi_commons.force_date=usi_commons.gup_or_get_cookie("usi_force_date"),usi_commons.force_group=usi_commons.gup_or_get_cookie("usi_force_group"),usi_commons.is_enabled=""!=usi_commons.gup_or_get_cookie("usi_enable",usi_cookies.expire_time.hour,!0),usi_commons.is_forced=""!=usi_commons.gup_or_get_cookie("usi_force",usi_cookies.expire_time.hour,!0),""!=usi_commons.gup("usi_email_id")?usi_cookies.set("usi_email_id",usi_commons.gup("usi_email_id").split(".")[0],Number(usi_commons.gup("usi_email_id").split(".")[1]),!0):null==usi_cookies.read_cookie("usi_email_id")&&null!=usi_cookies.get_from_window_name("usi_email_id")&&usi_cookies.set("usi_email_id",usi_cookies.get_from_window_name("usi_email_id")[0],(usi_cookies.get_from_window_name("usi_email_id")[1]-new Date().getTime())/1e3,!0),""!=usi_commons.gup_or_get_cookie("usi_debug")&&(usi_commons.debug=!0),""!=usi_commons.gup_or_get_cookie("usi_qa")&&(usi_commons.domain=usi_commons.cdn="https://prod.upsellit.com"),usi_cookies.monitor_page_views()}catch(e){usi_commons.report_error(e)}-1!=location.href.indexOf("usi_clearcookies")&&usi_cookies.flush(),usi_commons.objects=["product_rec","product","product_recs","abandon_recs","base_products","buypage_addons","campaign_56959","cart_items","cart_recs","cart_upsell_recs","cross_sell_products","discontinued_rec","filter_rec0","inpage_data","minicart_rec","minicart_recs","newproducts_data","oos_data","oos_rec","oos_rec_data","pdpbundler_recs","prod_27450","product_rec_cart","product_rec_minicart","product_rec_oos","rec_48323","rec_58915","rec_58917","rec_58921","rec_cart_items","recs","recs_34089","recs_51731","search_rec","toppicks","toppicks_customizations","topproducts_data","trade_up_products","variant_group_0","variant_group_1","variant_group_2","variant_group_3","variant_group_4","variant_group_5","variant_group_6","variant_group_7","variant_group_8","variant_group_9"],usi_commons.check_for_back_clicked=function(){try{if("undefined"!=typeof usi_app&&null!=usi_cookies.get("usi_back_clicked")&&window.self===window.top&&(void 0===usi_app.last_back_url||usi_app.last_back_url!=location.href)){usi_app.last_back_url=location.href,void 0!==usi_app.common_objects&&(usi_commons.objects=usi_commons.objects.concat(usi_app.common_objects)),usi_cookies.get("usi_record_rec_names")&&(usi_commons.objects=usi_commons.objects.concat(usi_cookies.get("usi_record_rec_names").split(",")));for(var e=0;e<usi_commons.objects.length;e++)null!=usi_cookies.get("usi_app_"+usi_commons.objects[e])&&(usi_app[usi_commons.objects[e]]=JSON.parse(usi_cookies.get("usi_app_"+usi_commons.objects[e])));var r=usi_cookies.get("usi_back_clicked").split("_");3===r.length&&usi_commons.load_view(r[0],r[1],"configID:"+r[2],function(){usi_js.cleanup=function(){}});return}setTimeout(usi_commons.check_for_back_clicked,1e3)}catch(t){usi_commons.report_error(t)}},setTimeout(usi_commons.check_for_back_clicked,10)}
"undefined"==typeof usi_dom&&((usi_dom={}).get_elements=function(e,t){var n=[];return t=t||document,n=Array.prototype.slice.call(t.querySelectorAll(e))},usi_dom.get_first_element=function(e,t){if(""===(e||""))return null;if(t=t||document,"[object Array]"!==Object.prototype.toString.call(e))return t.querySelector(e);for(var n=null,r=0;r<e.length;r++){var i=e[r];if(null!=(n=usi_dom.get_first_element(i,t)))break}return n},usi_dom.get_element_text_no_children=function(e,t){var n="";if(null==t&&(t=!1),null!=(e=e||document)&&null!=e.childNodes)for(var r=0;r<e.childNodes.length;++r)3===e.childNodes[r].nodeType&&(n+=e.childNodes[r].textContent);return!0===t&&(n=usi_dom.clean_string(n)),n.trim()},usi_dom.clean_string=function(e){return"string"!=typeof e?void 0:(e=(e=(e=(e=(e=(e=(e=e.replace(/[\u2010-\u2015\u2043]/g,"-")).replace(/[\u2018-\u201B]/g,"'")).replace(/[\u201C-\u201F]/g,'"')).replace(/\u2024/g,".")).replace(/\u2025/g,"..")).replace(/\u2026/g,"...")).replace(/\u2044/g,"/")).replace(/[^\x20-\xFF\u0100-\u017F\u0180-\u024F\u20A0-\u20CF]/g,"").trim()},usi_dom.string_to_decimal=function(e){var t=null;if("string"==typeof e)try{var n=parseFloat(e.replace(/[^0-9\.-]+/g,""));!1===isNaN(n)&&(t=n)}catch(r){usi_commons.log("Error: "+r.message)}return t},usi_dom.string_to_integer=function(e){var t=null;if("string"==typeof e)try{var n=parseInt(e.replace(/[^0-9-]+/g,""));!1===isNaN(n)&&(t=n)}catch(r){usi_commons.log("Error: "+r.message)}return t},usi_dom.get_absolute_url=function(){var e;return function(t){return(e=e||document.createElement("a")).href=t,e.href}}(),usi_dom.format_currency=function(e,t,n){var r="";return isNaN(e)&&(e=usi_dom.currency_to_decimal(e)),!1===isNaN(e)&&("object"==typeof Intl&&"function"==typeof Intl.NumberFormat?(t=t||"en-US",n=n||{style:"currency",currency:"USD"},r=Number(e).toLocaleString(t,n)):r=e),r},usi_dom.currency_to_decimal=function(e){return 0==e.indexOf("&")&&-1!=e.indexOf(";")?e=e.substring(e.indexOf(";")+1):-1!=e.indexOf("&")&&-1!=e.indexOf(";")&&(e=e.substring(0,e.indexOf("&"))),isNaN(e)&&(e=e.replace(/[^0-9,.]/g,"")),e.indexOf(",")==e.length-3&&(-1!=e.indexOf(".")&&(e=e.replace(".","")),e=e.replace(",",".")),e=e.replace(/[^0-9.]/g,"")},usi_dom.to_decimal_places=function(e,t){if(null==e||"number"!=typeof e||null==t||"number"!=typeof t)return null;if(0==t)return parseFloat(Math.round(e));for(var n=10,r=1;r<t;r++)n*=10;return parseFloat(Math.round(e*n)/n)},usi_dom.trim_string=function(e,t,n){return n=n||"",(e=e||"").length>t&&(e=e.substring(0,t),""!==n&&(e+=n)),e},usi_dom.attach_event=function(e,t,n){var r=usi_dom.find_supported_element(e,n);usi_dom.detach_event(e,t,r),r.addEventListener?r.addEventListener(e,t,!1):r.attachEvent("on"+e,t)},usi_dom.detach_event=function(e,t,n){var r=usi_dom.find_supported_element(e,n);r.removeEventListener?r.removeEventListener(e,t,!1):r.detachEvent("on"+e,t)},usi_dom.find_supported_element=function(e,t){return(t=t||document)===window?window:!0===usi_dom.is_event_supported(e,t)?t:t===document?window:usi_dom.find_supported_element(e,document)},usi_dom.is_event_supported=function(e,t){return null!=t&&void 0!==t["on"+e]},usi_dom.is_defined=function(e,t){if(null==e||""===(t||""))return!1;var n=!0,r=e;return t.split(".").forEach(function(e){!0===n&&(null==r||"object"!=typeof r||!1===r.hasOwnProperty(e)?n=!1:r=r[e])}),n},usi_dom.ready=function(e){void 0!==document.readyState&&"complete"===document.readyState?e():window.addEventListener?window.addEventListener("load",e,!0):window.attachEvent?window.attachEvent("onload",e):setTimeout(e,5e3)},usi_dom.fit_text=function(e,t){t||(t={});var n={multiLine:!0,minFontSize:.1,maxFontSize:20,widthOnly:!1},r={};for(var i in n)t.hasOwnProperty(i)?r[i]=t[i]:r[i]=n[i];var l=Object.prototype.toString.call(e);function o(e,t){a=e.innerHTML,d=parseInt(window.getComputedStyle(e,null).getPropertyValue("font-size"),10),c=(n=e,r=window.getComputedStyle(n,null),(n.clientWidth-parseInt(r.getPropertyValue("padding-left"),10)-parseInt(r.getPropertyValue("padding-right"),10))/d),u=(i=e,l=window.getComputedStyle(i,null),(i.clientHeight-parseInt(l.getPropertyValue("padding-top"),10)-parseInt(l.getPropertyValue("padding-bottom"),10))/d),c&&(t.widthOnly||u)||(t.widthOnly?usi_commons.log("Set a static width on the target element "+e.outerHTML):usi_commons.log("Set a static height and width on the target element "+e.outerHTML)),-1===a.indexOf("textFitted")?((o=document.createElement("span")).className="textFitted",o.style.display="inline-block",o.innerHTML=a,e.innerHTML="",e.appendChild(o)):o=e.querySelector("span.textFitted"),t.multiLine||(e.style["white-space"]="nowrap"),f=t.minFontSize,s=t.maxFontSize;for(var n,r,i,l,o,u,a,c,d,f,p,s,$=f,g=1e3;f<=s&&g>0;)g--,p=s+f-.1,o.style.fontSize=p+"em",o.scrollWidth/d<=c&&(t.widthOnly||o.scrollHeight/d<=u)?($=p,f=p+.1):s=p-.1;o.style.fontSize!==$+"em"&&(o.style.fontSize=$+"em")}"[object Array]"!==l&&"[object NodeList]"!==l&&"[object HTMLCollection]"!==l&&(e=[e]);for(var u=0;u<e.length;u++)o(e[u],r)});
"undefined"==typeof usi_aff&&(usi_aff={fix_linkshare:function(){try{if(""!=usi_commons.gup("ranSiteID")&&(usi_aff.log_url(),-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))){usi_cookies.del("usi_clicked_1");var e=new Date,i=e.getUTCFullYear()+(e.getUTCMonth()+1<10?"0":"")+(e.getUTCMonth()+1)+(10>e.getUTCDate()?"0":"")+e.getDate(),c=(10>e.getUTCHours()?"0":"")+e.getUTCHours()+(10>e.getUTCMinutes()?"0":"")+e.getUTCMinutes();usi_cookies.create_nonencoded_cookie("usi_rmStore","ald:"+i+"_"+c+"|atrv:"+usi_commons.gup("ranSiteID"),usi_cookies.expire_time.month)}null!=usi_cookies.read_cookie("usi_rmStore")&&(usi_cookies.create_nonencoded_cookie("rmStore",usi_cookies.read_cookie("usi_rmStore"),usi_cookies.expire_time.month),localStorage.setItem("rmStore",'{"/":"'+usi_cookies.read_cookie("usi_rmStore")+'"}'))}catch(r){usi_commons.report_error(r)}},fix_cj:function(){try{if(""!=usi_commons.gup("cjevent")||""!=usi_commons.gup("CJEVENT")){usi_aff.log_url(),usi_cookies.del("cjUser");var e=usi_commons.gup("cjevent");""==e&&(e=usi_commons.gup("CJEVENT")),(-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))&&(usi_cookies.del("usi_clicked_1"),usi_cookies.create_nonencoded_cookie("usi_cjevent",e,usi_cookies.expire_time.month,!0))}null!=usi_cookies.read_cookie("usi_cjevent")&&(usi_cookies.create_nonencoded_cookie("cjevent",usi_cookies.read_cookie("usi_cjevent"),usi_cookies.expire_time.month,!0),usi_cookies.create_nonencoded_cookie("cjevent_dc",usi_cookies.read_cookie("usi_cjevent"),usi_cookies.expire_time.month,!0),usi_cookies.create_nonencoded_cookie("cje",usi_cookies.read_cookie("usi_cjevent"),usi_cookies.expire_time.month,!0),localStorage.setItem("cjevent",usi_cookies.read_cookie("usi_cjevent")),sessionStorage.setItem("cjevent",usi_cookies.read_cookie("usi_cjevent")))}catch(i){usi_commons.report_error(i)}},fix_sas:function(){try{""!=usi_commons.gup("sscid")&&(usi_aff.load_script("https://www.upsellit.com/launch/blank.jsp?aff_click_sas="+encodeURIComponent(location.href)),(-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))&&(usi_cookies.del("usi_clicked_1"),usi_cookies.create_nonencoded_cookie("usi_sscid",usi_commons.gup("sscid"),usi_cookies.expire_time.month))),null!=usi_cookies.read_cookie("usi_sscid")&&usi_cookies.create_nonencoded_cookie("sas_m_awin",'{"clickId":"'+usi_cookies.read_cookie("usi_sscid")+'"}',usi_cookies.expire_time.month)}catch(e){usi_commons.report_error(e)}},fix_awin:function(e){try{""!=usi_commons.gup("awc")&&(usi_aff.log_url(),(-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))&&(usi_cookies.del("usi_clicked_1"),usi_cookies.create_nonencoded_cookie("usi_awc",usi_commons.gup("awc"),usi_cookies.expire_time.month),usi_cookies.del("_aw_j_"+e))),null!=usi_cookies.read_cookie("usi_awc")&&(usi_cookies.del("_aw_j_"+e),usi_cookies.create_nonencoded_cookie("AwinChannelCookie","aw",2592e3,!0),usi_cookies.create_nonencoded_cookie("AwinCookie","aw",2592e3,!0),usi_cookies.create_nonencoded_cookie("awin_source","aw",2592e3,!0),usi_cookies.create_nonencoded_cookie("_aw_m_"+e,usi_cookies.read_cookie("usi_awc"),usi_cookies.expire_time.month),usi_cookies.create_nonencoded_cookie("awc",usi_cookies.read_cookie("usi_awc"),usi_cookies.expire_time.month),"undefined"!=typeof AWIN&&void 0!==AWIN.Tracking&&void 0!==AWIN.Tracking.StorageProvider&&AWIN.Tracking.StorageProvider.setAWC(e,usi_cookies.read_cookie("usi_awc")))}catch(i){usi_commons.report_error(i)}},fix_pj:function(){try{if(""!=usi_commons.gup("clickId")&&(usi_aff.log_url(),-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))){usi_cookies.del("usi_clicked_1");var e=new Date;usi_cookies.create_nonencoded_cookie("usi-pjn-click",'[{"id":"'+usi_commons.gup("clickId")+'","days":'+Math.floor(e/864e5)+',"type":"p"}]',usi_cookies.expire_time.month)}null!=usi_cookies.read_cookie("usi-pjn-click")&&(usi_cookies.create_nonencoded_cookie("pjn-click",usi_cookies.read_cookie("usi-pjn-click"),usi_cookies.expire_time.month),localStorage.setItem("pjnClickData",usi_cookies.read_cookie("usi-pjn-click")))}catch(i){usi_commons.report_error(i)}},fix_ir:function(e){try{if((""!=usi_commons.gup("irclickid")||""!=usi_commons.gup("clickid")||""!=usi_commons.gup("im_ref"))&&(usi_aff.log_url(),-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))){usi_cookies.del("usi_clicked_1");var i=usi_commons.gup("irclickid");""==i&&(i=usi_commons.gup("clickid")),""==i&&(i=usi_commons.gup("im_ref"));var c=Date.now().toString(),r=c+"|-1|"+c+"|"+i+"|";usi_cookies.create_nonencoded_cookie("usi_IR_"+e,r,usi_cookies.expire_time.month)}null!=usi_cookies.read_cookie("usi_IR_"+e)&&(usi_cookies.create_nonencoded_cookie("IR_"+e,usi_cookies.read_cookie("usi_IR_"+e),usi_cookies.expire_time.month),usi_cookies.create_nonencoded_cookie("irclickid",usi_cookies.read_cookie("usi_IR_"+e).split("|")[3],usi_cookies.expire_time.month))}catch(o){usi_commons.report_error(o)}},fix_cf:function(){try{""!=usi_commons.gup("cfclick")&&(usi_aff.log_url(),(-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))&&(usi_cookies.del("usi_clicked_1"),usi_cookies.create_nonencoded_cookie("usi-cfjump-click",usi_commons.gup("cfclick"),usi_cookies.expire_time.month))),null!=usi_cookies.read_cookie("usi-cfjump-click")&&(usi_cookies.create_nonencoded_cookie("cfjump-click",usi_cookies.read_cookie("usi-cfjump-click"),usi_cookies.expire_time.month),usi_cookies.create_nonencoded_cookie("cfclick",usi_cookies.read_cookie("usi-cfjump-click"),usi_cookies.expire_time.month))}catch(e){usi_commons.report_error(e)}},fix_avantlink:function(){try{""!=usi_commons.gup("avad")&&(usi_aff.log_url(),(-1!=location.href.indexOf("usi_email_id")||null!=usi_cookies.get("usi_clicked_1"))&&(usi_cookies.del("usi_clicked_1"),usi_cookies.create_nonencoded_cookie("usi_avad",usi_commons.gup("avad"),usi_cookies.expire_time.month),usi_aff.wait_for_avmws=function(){null!=usi_cookies.get("avmws")?usi_cookies.create_nonencoded_cookie("usi_avmws",usi_cookies.get("avmws"),usi_cookies.expire_time.month):setTimeout(usi_aff.wait_for_avmws,1e3)},usi_aff.wait_for_avmws())),null!=usi_cookies.read_cookie("usi_avmws")&&usi_cookies.create_nonencoded_cookie("avmws",usi_cookies.read_cookie("usi_avmws"),usi_cookies.expire_time.month)}catch(e){usi_commons.report_error(e)}},get_impact_pixel:function(){var e="";try{for(var i=document.getElementsByTagName("script"),c=0;c<i.length;c++){var r=i[c].innerText;if(r&&(-1!=r.indexOf("ire('trackConversion'")||-1!=r.indexOf('ire("trackConversion"'))){e=(e=(e=r.trim().replace(/\s/g,"")).split("trackConversion")[1]).split("});")[0];break}}}catch(o){usi_commons.report_error(o)}return e},log_url:function(){usi_aff.load_script("https://www.upsellit.com/launch/blank.jsp?aff_click="+encodeURIComponent(location.href))},monitor_affiliate_pixel:function(e){try{var i=usi_aff.report_affiliate_pixels();if(i)return"function"==typeof e&&e(i),usi_aff.parse_pixels(i);setTimeout(function(){usi_aff.monitor_affiliate_pixel(e)},1e3)}catch(c){usi_commons.report_error(c)}},parse_pixels:function(e){try{usi_aff.load_script("https://www.upsellit.com/launch/blank.jsp?pixel_found="+encodeURIComponent(location.href)+"&"+e)}catch(i){usi_commons.report_error(i)}},report_affiliate_pixels:function(){var e="";try{var i={cj:document.querySelector("[src*='emjcd.com']"),sas:document.querySelector("[src*='shareasale.com/sale.cfm']"),linkshare:document.querySelector("[src*='track.linksynergy.com']"),pj:document.querySelector("[src*='t.pepperjamnetwork.com/track']"),avant:document.querySelector("[src*='tracking.avantlink.com/ptcfp.php']"),ir:{src:usi_aff.get_impact_pixel()},awin1:document.querySelector("[src*='awin1.com/sread']"),awin2:document.querySelector("[src*='zenaps.com/sread.js']"),cf:document.querySelector("[src*='https://cfjump.'][src*='.com/track']"),saasler1:document.querySelector("[src*='engine.saasler.com']"),saasler2:document.querySelector("[src*='saasler-impact.herokuapp.com']")};for(var c in i)i[c]&&i[c].src&&(e+="&"+c+"="+encodeURIComponent(i[c].src))}catch(r){usi_commons.report_error(r)}return e},load_script:function(e){try{var i=document.getElementsByTagName("head")[0],c=document.createElement("script");c.type="text/javascript",c.src=e,i.appendChild(c)}catch(r){usi_commons.report_error(r)}}});
"undefined"==typeof usi_company&&(window.usi_company={rulesets:{testing:function(e){return void 0===e.testing||(e.testing?usi_cookies.get("usi_enable"):e.testing?void 0:!usi_cookies.get("usi_enable"))},device:function(e){return!e.device||usi_commons.device===e.device},required_cookies:function(e){return!e.required_cookies||usi_cookies.value_exists.apply(null,e.required_cookies)},suppress_cookies:function(e){if(!e.suppress_cookies)return!0;for(var s=0;s<e.suppress_cookies.length;s++)if(usi_cookies.value_exists(e.suppress_cookies[s]))return!1;return!0},required_elements:function(e){if(!e.required_elements)return!0;try{for(var s=0;s<e.required_elements.length;s++)if(!document.querySelector(e.required_elements[s]))return!1;return!0}catch(e){return!1}},min_subtotal:function(e){return void 0===e.min_subtotal||usi_company.get_subtotal()>e.min_subtotal},max_subtotal:function(e){return void 0===e.max_subtotal||usi_company.get_subtotal()<e.max_subtotal},subtotal_gt:function(e){return void 0===e.subtotal_gt||usi_company.get_subtotal()>e.subtotal_gt},subtotal_lt:function(e){return void 0===e.subtotal_lt||usi_company.get_subtotal()<e.subtotal_lt},subtotal_gte:function(e){return void 0===e.subtotal_gte||usi_company.get_subtotal()>=e.subtotal_gte},subtotal_lte:function(e){return void 0===e.subtotal_lte||usi_company.get_subtotal()<=e.subtotal_lte},date_ranges:function(e){return e.date_ranges&&"undefined"==typeof usi_date?usi_commons.log("usi_date is required"):!e.date_ranges||e.date_ranges.some(function(e){return usi_date.is_date(new Date(e[1]))&&!usi_date.is_date(new Date(e[0]))?usi_date.is_before(e[1]):usi_date.is_date(new Date(e[0]))&&!usi_date.is_date(new Date(e[1]))?usi_date.is_after(e[0]):usi_date.is_between(e[0],e[1])})},is_after:function(e){return e.is_after&&"undefined"==typeof usi_date?usi_commons.log("usi_date is required"):!e.is_after||usi_date.is_after(e.is_after)},is_before:function(e){return e.is_before&&"undefined"==typeof usi_date?usi_commons.log("usi_date is required"):!e.is_before||usi_date.is_before(e.is_before)},is_entry:function(e){if(void 0===e.is_entry)return!0;var s=usi_cookies.get("usi_referrer_url"),i=document.referrer==s||""==document.referrer&&"direct traffic"==s,t=location.href==usi_cookies.get("usi_entry_url_1")&&i;return e.is_entry===t},page_visits:function(e){if(void 0===e.page_visits)return!0;var s=Number(usi_cookies.get("usi_pv_count"));return("number"!=typeof e.page_visits.equals||s===e.page_visits.equals)&&(!("number"==typeof e.page_visits.min&&s<e.page_visits.min)&&!("number"==typeof e.page_visits.max&&s>e.page_visits.max))},countries:function(e){return e.countries&&!usi_app.country?usi_commons.log("usi_app.country is required"):!e.countries||-1!==e.countries.indexOf(usi_app.country)},states:function(e){return e.states&&!usi_app.state?usi_commons.log("usi_app.state is required"):!e.states||-1!==e.states.indexOf(usi_app.state)},suppress_countries:function(e){return e.suppress_countries&&!usi_app.country?usi_commons.log("usi_app.country is required"):!e.suppress_countries||-1===e.suppress_countries.indexOf(usi_app.country)},suppress_states:function(e){return e.suppress_states&&!usi_app.state?usi_commons.log("usi_app.state is required"):!e.suppress_states||-1===e.suppress_states.indexOf(usi_app.state)},traffic_percent:function(e){return void 0===e.traffic_percent||(e.siteID&&!usi_cookies.get("usi_traffic"+e.siteID)&&usi_cookies.set("usi_traffic"+e.siteID,Math.random()>e.traffic_percent?"true":"false"),e.siteID&&"true"===usi_cookies.get("usi_traffic"+e.siteID))},traffic_source:function(e){return void 0===e.traffic_source||(usi_cookies.get("usi_traffic_source")||usi_commons.log_error("usi_traffic_source required"),""===usi_cookies.get("usi_traffic_source")&&-1!==e.traffic_source.indexOf("direct")||e.traffic_source.some(function(e){return-1!==usi_cookies.get("usi_traffic_source").indexOf(e)}))},pages:function(e){return void 0===e.pages||e.pages.some(function(e){return"/"===e?location.pathname==e:-1!==location.href.indexOf(e)})},suppressed_pages:function(e){return void 0===e.suppressed_pages||!e.suppressed_pages.some(function(e){return"/"===e?location.pathname==e:-1!==location.href.indexOf(e)})},logged_in:function(e){return void 0===e.logged_in||(e.logged_in?"loggedin"===usi_cookies.get("usi_visitor"):e.logged_in?void 0:"loggedin"!==usi_cookies.get("usi_visitor"))},logged_out:function(e){return void 0===e.logged_out||(e.logged_out?"loggedin"!==usi_cookies.get("usi_visitor"):e.logged_out?void 0:"loggedin"===usi_cookies.get("usi_visitor"))},return_visitor:function(e){if(void 0===e.return_visitor)return!0;if("undefined"==typeof usi_date)return usi_commons.log("usi_date is required");var s=usi_commons.gup_or_get_cookie("usi_force_return");if("1"===s||"0"===s)return"1"===s===e.return_visitor;var i=usi_company.is_return("number"==typeof e.return_visitor?e.return_visitor:24);return e.return_visitor?i:!i},new_visitor:function(e){if(void 0===e.new_visitor)return!0;if("undefined"==typeof usi_date)return usi_commons.log("usi_date is required");var s=usi_commons.gup_or_get_cookie("usi_force_return");if("1"===s||"0"===s)return"0"===s===e.new_visitor;var i=usi_company.is_return("number"==typeof e.new_visitor?e.new_visitor:24);return e.new_visitor?!i:i},last_purchase:function(e){if(void 0===e.last_purchase)return!0;var s=Number(usi_cookies.get("usi_customer_purchased"));return e.last_purchase.equals?e.last_purchase.equals==s:e.last_purchase.min?e.last_purchase.min>=s:!!e.last_purchase.max&&e.last_purchase.max<=s},return_customer:function(e){return void 0===e.return_customer||(e.return_customer?usi_cookies.get("usi_customer_purchased"):e.return_customer?void 0:!usi_cookies.get("usi_customer_purchased"))},new_customer:function(e){return void 0===e.new_customer||(e.new_customer?!usi_cookies.get("usi_customer_purchased"):e.new_customer?void 0:usi_cookies.get("usi_customer_purchased"))}},get_subtotal:function(){return usi_cookies.get("usi_subtotal")?Number(usi_cookies.get("usi_subtotal").replace(/[^0-9.]/g,"")):0},is_return:function(e){if("undefined"==typeof usi_date)return usi_commons.log("usi_date is required");var s=!1,i="usi_return_visitor",t=usi_date.set_date();!1===usi_cookies.value_exists(i)&&usi_cookies.set(i,t,usi_cookies.expire_time.never,!0);var o=new Date(usi_cookies.get(i));return usi_date.is_date(o)&&(s=usi_date.diff(o,t,"hours",2)>=e),s},test_load:function(e,s){return!1},before_load:async function(e){usi_commons.log("Loading: "+(e._name?e._name+", ":e.name?e.name+", ":"")+(e.siteID?e.siteID+", ":"")+(e.key?e.key:"")),"string"==typeof e.before_load&&"function"==typeof usi_app[e.before_load]&&await usi_app[e.before_load](e)},on_load:function(e,s){"object"==typeof e&&e.on_load&&("object"==typeof s&&"function"==typeof s[e.on_load]?s[e.on_load]():"object"==typeof usi_app&&"function"==typeof usi_app[e.on_load]&&usi_app[e.on_load]())},post_load_campaigns:function(e){if("1"==usi_commons.gup_or_get_cookie("usi_testing")&&e.campaigns){var s=Object.keys(usi_company.rulesets);s=s.concat(Object.keys(usi_company.custom_rulesets)),s=Array.from(new Set(s)).sort();var i={};for(var t in e.campaigns)i[t.charAt(0)]=e.campaigns[t].map(function(e){return e._missing?e._missing.map(e=>s.indexOf(e)):-1});var o=JSON.stringify(i),u=JSON.stringify(s),r=JSON.stringify(e);o!=sessionStorage.usi_campaign_results&&sessionStorage.setItem("usi_campaign_results",o),u!=sessionStorage.usi_campaign_keys&&(sessionStorage.usi_campaign_json||sessionStorage.setItem("usi_campaign_json",r),sessionStorage.setItem("usi_campaign_keys",u))}},load_campaigns:function(e,s){try{if(!e||!e.campaigns)return;function i(e,s){var i=0;!function t(){if(!(i>=e.length)){var o=e[i++];s(o,function(e){e||t()})}}()}function t(e,s,i){if(!e)return"";var t=e.match(/^{{\s*usi_app\.([\w.]+)\s*}}$/);if(t){var o=t[1].split(".");let u=usi_app;for(let s of o){if(null==u||"object"!=typeof u)return e;u=u[s]}return"function"==typeof u?u(i||s):u}return e.replace(/{{\s*usi_commons\.device\s*}}/,usi_commons.device).replace(/{{\s*usi_app\.([\w.]+)\s*}}/g,function(e,s){if(!s)return e;for(var t=s.split("."),o=usi_app,u=0;u<t.length;u++){if(null==o||"object"!=typeof o)return e;o=o[t[u]]}return null==o?e:"function"==typeof o?o(i):o})}function o(e,s){var i=Object.assign({},e);for(var o in i)i.hasOwnProperty(o)&&"string"==typeof i[o]&&i[o].match(/{{\s*usi_app\.([\w.]+)\s*}}/)&&(i[o]=t(i[o],i,s));return i}function u(e,s){try{var i=[],u={};if(e.segments&&Array.isArray(e.segments))for(var r=0;r<e.segments.length;r++){var n=e.segments[r],a=[];for(var _ in n)if(n.hasOwnProperty(_)){var c=usi_company.custom_rulesets[_]||usi_company.rulesets[_];for(var p in"function"!=typeof c||c(Object.assign({},e,n))||a.push(_),usi_company.custom_rulesets){if(usi_company.custom_rulesets.hasOwnProperty(p))(0,usi_company.custom_rulesets[p])({...e,...n})||a.push(p)}}if(0===a.length){u=n;break}}var f=Object.assign({},e,u);for(var l in"view"===f._type&&"undefined"==typeof usi_force&&-1==location.href.indexOf("usi_force")&&(f.suppress_cookies=f.suppress_cookies||[],-1===f.suppress_cookies.indexOf("usi_sale")&&f.suppress_cookies.push("usi_sale","usi_launched","usi_launched"+f.siteID),e.suppress_cookies=f.suppress_cookies),usi_company.rulesets){if(!usi_company.custom_rulesets[l]&&usi_company.rulesets.hasOwnProperty(l))(0,usi_company.rulesets[l])(f)||i.push(l)}for(var m in usi_company.custom_rulesets){if(usi_company.custom_rulesets.hasOwnProperty(m))(0,usi_company.custom_rulesets[m])(f)||i.push(m)}if(e._missing=i,i.length>0)return s(!1);var d=[];if(f.list){if(!usi_app.company_id)return usi_commons.log_error("usi_app.company_id is required");if(!f.list.ids)return usi_commons.log_error("campaign.list.ids is required");if(!f.list.label)return usi_commons.log_error("campaign.list.label is required");d.push(function(s){var u=o(f.list,f);if(f.product=Array.isArray(u.ids)?u.ids.join(","):t(u.ids,f),f.save_token="usi_ls_"+f.list.label+"_"+f.product,sessionStorage[f.save_token])return s("true"===sessionStorage[f.save_token]);usi_company.lookup_callback=function(t){try{e.list._found=t,u.type=u.type||"suppress";var o=0===t&&"suppress"===u.type||1===t&&"enable"===u.type;sessionStorage.setItem(f.save_token,o.toString()),o||i.push("list"),s(o)}catch(e){usi_commons.report_error(e)}};var r=usi_commons.domain+"/utility/lookup_suppressions.jsp?companyID="+usi_app.company_id+"&product="+f.product+"&label="+u.label+"&match="+(u.match||"any")+"&callback=usi_company.lookup_callback";usi_commons.load_script(r)})}if(f.lift){if("undefined"==typeof usi_split_test)return usi_commons.log_error("usi_split_test is required");if(!f.lift.id)return usi_commons.log_error("campaign.lift.id is required");d.push(function(s){usi_split_test.instantiate_callback(f.lift.id,function(t){if(0==t)return f.lift.ghost?(f={...f,...f.lift.ghost},s(!0)):(i.push("lift"),s(!1));e.lift._group=t,s(!0)})})}"object"==typeof f.split&&d.push(function(s){var i,t=Object.keys(f.split),o=usi_commons.gup("usi_force_group");if(o)i=o;else if(f._group)i=f._group;else if(f.lift&&"boolean"==typeof f.lift.split&&f.lift.split&&f.lift._group)i=f.lift._group;else{for(var u=0,r={},n=0;n<t.length;n++){var a=t[n],_=f.split[a].percent;r[a]="number"==typeof _&&_>0?_:1,u+=r[a]}for(var c=Math.random()*u,p=0,l=0;l<t.length;l++){var m=t[l];if(c<(p+=r[m])){i=m;break}}i||(i=t[0])}var d=f.split[i];for(var g in d)d.hasOwnProperty(g)&&(f[g]=d[g]);e._group=i,s(!0)}),d.push(function(e){if(!f.recommendations)return e(!0);const s=o(f.recommendations,f);return s.pid?s.siteID?(s.callback=async function(s){try{f.recommendations.filter_callback&&"function"==typeof usi_app[f.recommendations.filter_callback]&&await usi_app[f.recommendations.filter_callback](f);const t=f.recommendations.name?f.recommendations.name.replace("usi_app.",""):"product_rec",o=usi_app[t]&&usi_app[t].data&&usi_app[t].data.length?usi_app[t].data.length:0,u=void 0!==f.recommendations.min_rows?f.recommendations.min_rows:f.recommendations.rows?f.recommendations.rows:3,r=usi_commons.gup("usi_test")||o>=u;f.product_rec=s,r||i.push("recommendations"),e(r)}catch(s){usi_commons.log_error(s),e(!1)}},void usi_commons.load_products(s)):(usi_commons.log_error("recommendations.siteID is required"),e(!1)):(usi_commons.log_error("recommendations.pid is required"),e(!1))}),function(e,s){var i=0;!function t(o){return o?i>=e.length?s(!0):void e[i++](t):s(!1)}(!0)}(d,function(e){f.siteID||i.push("siteID"),"anon"==f._type||f.hash||i.push("hash"),s(e,f)})}catch(e){usi_commons.report_error(e),s(!1)}}usi_company.custom_rulesets=s||[],e.campaigns.usi_load&&i(e.campaigns.usi_load,function(e,s){e._type="usi_load",u(e,function(i,u){e._active=i,i&&u&&u.siteID&&u.hash?usi_company.before_load(u).then(function(){!1===usi_commons.load(u.hash,u.siteID,u.key?t(u.key,u):"",function(){var e=window["usi_"+u.siteID];void 0!==e&&(e.company_json=o(u),u.on_load&&usi_company.on_load(u,e)),s(usi_company.test_load(i,u))})&&s(usi_company.test_load(i,u))}):s(i)})}),e.campaigns.view&&i(e.campaigns.view,function(e,s){e._type="view",u(e,function(i,u){e._active=i,i&&u&&u.siteID&&u.hash&&usi_company.before_load(u).then(function(){usi_commons.load_view(u.hash,u.siteID,u.key?t(u.key,u):"",function(){"undefined"!=typeof usi_js&&(usi_js.company_json=o(u),u.on_load&&usi_company.on_load(u,usi_js))})}),s(i)})}),e.campaigns.anon&&i(e.campaigns.anon,function(e,s){e._type="anon",u(e,function(i,t){e._active=i,i&&t&&t.siteID&&(usi_app.anon_data=o(t),usi_company.before_load(t).then(function(){if("undefined"==typeof usi_user_id)return usi_commons.log_error("usi_user_id is required");t.found_user_callback&&"function"==typeof usi_app[t.found_user_callback]&&(usi_user_id.found_user_callback=usi_app[t.found_user_callback]),usi_user_id.activate(t.siteID),t.on_load&&usi_company.on_load(t,usi_user_id)})),s(i)})}),e.campaigns.precapture&&i(e.campaigns.precapture,function(e,s){e._type="precapture",u(e,function(i,t){e._active=i,i&&t&&t.siteID&&t.hash&&(usi_app.precapture_data=o(t),usi_company.before_load(t).then(function(){usi_commons.load_precapture(t.hash,t.siteID,function(){t.on_load&&usi_company.on_load(t,usi_js_monitor)})})),s(i)})}),usi_company.post_load_campaigns()}catch(r){usi_commons.report_error(r)}}});
if (typeof usi_company_json === 'undefined') {try {usi_company_json = {
  "campaigns": {
    "view": [
      {
        "name": "Udemy Active Cart Engagement",
        "siteID": "62737",
        "hash": "ZFjjJe4NuelUB28WzlAXnOy",
        "key": "{{usi_commons.device}}",
        "suppressed_pages": [
          "/"
        ],
        "required_cookies": [
          "usi_pids",
          "usi_traffic_source"
        ],
        "list": {
          "ids": "{{usi_app.get_pids}}",
          "label": "Udemy course List - March 2026",
          "match": "any",
          "type": "enable"
        }
      }
    ]
  }
};} catch (err) {usi_commons.report_error(err);}}

		usi_app = {};
		usi_app.main = function () {
			try {
				if (window.self !== window.top) return;
				usi_app.company_id = "6885";
				usi_app.url = location.href.toLowerCase();
				usi_app.coupon = usi_cookies.value_exists("usi_coupon_applied") ? "" : usi_commons.gup_or_get_cookie("usi_coupon", usi_cookies.expire_time.week, true);
				
				// Pages
				usi_app.is_cart_page = /\/cart\//.test(usi_app.url);
				usi_app.is_checkout_page = /\/subscription-checkout\//.test(usi_app.url);
				usi_app.is_confirmation_page = usi_app.url.match("/cart/success/") != null;
				usi_app.is_pdp_page = /udemy\.com\/course\/[^\/]+/.test(usi_app.url);
				usi_app.detect_traffic_source();
	
				// Booleans
				usi_app.is_suppressed = !usi_app.is_forced && (usi_app.url.match("udemy") == null ||
					usi_app.is_confirmation_page ||
					usi_cookies.value_exists("usi_sale"));
				
				// Suppress on 404 pages
				if (document.title.indexOf('404') != -1) return;
				
				// Load pixel on confirmation page
				if (usi_app.is_confirmation_page && typeof USI_orderID == "undefined") {
					usi_commons.load_script("//www.upsellit.com/active/udemy_pixel.jsp");
				}
				
				usi_aff.fix_linkshare();
				usi_aff.monitor_affiliate_pixel(function(){
					if (typeof USI_orderID == "undefined") {
						usi_commons.load_script("//www.upsellit.com/active/udemy_pixel.jsp");
					}
				});

				if (usi_app.is_suppressed) {
					return usi_commons.log("usi_app.main is suppressed.");
				}

				// Load boost bar
				if (usi_cookies.value_exists("usi_boostbar")) {
					usi_app.boostbar.load();
				}
				
				// Apply coupons
				if ((usi_app.is_checkout_page) && usi_app.coupon != "") {//usi_app.is_pdp_page || 
					usi_app.apply_coupon();
					return;
				}

				
				
				// Monitor PDP for product data
				if (usi_app.is_pdp_page && !usi_app.pdp_timeout) usi_app.start_pdp_monitor();
				usi_app.load();
			} catch(err) {
				usi_commons.report_error(err);
			}
		};
		
		usi_app.get_pids = function(){
			return usi_cookies.value_exists("usi_pids") ? usi_cookies.get("usi_pids").replaceAll("|", ",") : "";
		};

		usi_app.detect_traffic_source = function(){
			try {
				if (usi_cookies.value_exists("usi_traffic_source")) return;
				var is_affiliate =
					usi_commons.gup("utm_medium") == "affiliate" ||
					usi_commons.gup("ranSiteID") != "" ||
					usi_commons.gup("ranMID") != "" ||
					usi_commons.gup("LSNSUBSITE") != "" ||
					usi_commons.gup("irclickid") != "";
				if (is_affiliate) {
					usi_cookies.set("usi_traffic_source", "affiliate", usi_cookies.expire_time.day);
				}
			} catch(err) {
				usi_commons.report_error(err);
			}
		};

		usi_app.load = function () {
			try {
				usi_commons.log("usi_app.load()");
	
				if (typeof usi_js !== 'undefined' && typeof usi_js.cleanup === 'function') {
					usi_js.cleanup();
				}
				if (usi_app.is_suppressed) {
					return usi_commons.log("usi_app.load is suppressed");
				}
				if (!usi_app.is_pdp_page && !usi_cookies.value_exists("usi_prod_pid_1")) {
					return usi_commons.log("usi_app.load: no product data available");
				}
				
				usi_company.load_campaigns(usi_company_json);
				
			} catch(err) {
				usi_commons.report_error(err);
			}
		};
		
		usi_app.boostbar = {
			load: function(text){
				text = text || '';
				usi_commons.log("usi_app.boostbar.load()");
				if (usi_cookies.get("usi_boostbar") == "closed") return;

				var is_mobile = usi_commons.device === "mobile";
				var bg_image = is_mobile
					? 'https://www.upsellit.com/chatskins/6885/Udemy-TT-05-2026-boostbar-mbl-3x.webp'
					: 'https://www.upsellit.com/chatskins/6885/Udemy-TT-05-2026-boostbar-dsktp-3x.webp';
				var bar_padding = is_mobile ? '3.5em 2.5em' : '3em 2.5em';

				var usi_boost_css = [
					'#usi_boost_close {height:100%; width:5%; right:5%; top:0; bottom:0; position:absolute; color:#fff; font-size:2em; text-decoration:none;}',
					'#usi_boost_container {position:fixed; bottom:0; left:0; right:0; width:100%; text-align:center; background:#5A1FB8 url(' + bg_image + ') no-repeat center center; background-size:cover; color:#fff; padding:' + bar_padding + '; line-height:1; z-index:2147483647;}'
				].join('');
				usi_app.boostbar.place_css(usi_boost_css);

				var usi_boost_container = document.createElement('div');
				usi_boost_container.innerHTML = [
					'<div id="usi_boost_container">',
					'<a id="usi_boost_close" href="javascript:usi_app.boostbar.close();" aria-label="close">&times;</a>',
					'<span class="usi_sr_only">' + text + '</span>',
					'</div>'
				].join('');
				document.body.appendChild(usi_boost_container);
			},
			place_css:function(css) {
				usi_commons.log("usi_app.boostbar.place_css()");
				var usi_css = document.createElement("style");
				usi_css.type = "text/css";
				if (usi_css.styleSheet) usi_css.styleSheet.cssText = css;
				else usi_css.innerHTML = css;
				document.getElementsByTagName('head')[0].appendChild(usi_css);
			},
			close: function(){
				usi_commons.log("usi_app.boostbar.close()");
				var bar = document.getElementById('usi_boost_container');
				usi_cookies.set("usi_boostbar", "closed", usi_cookies.expire_time.week);
				if (bar != null) {
					bar.parentNode.removeChild(bar);
				}
			}
		};
		
		usi_app.apply_coupon = function() {
			try {
				usi_commons.log("usi_app.apply_coupon()");
				var coupon_input = null;
				var coupon_button = null;

				if (usi_app.is_pdp_page) {
					var container = document.querySelector('[data-purpose="redeem-coupon-container"]');
					if (container) {
						coupon_input = container.querySelector('[data-purpose="coupon-input"]');
						coupon_button = container.querySelector('form button[type="submit"]');
					}
					if (!coupon_input) {
						var show_btn = document.querySelector('[data-purpose="show-coupon-form"]');
						if (show_btn && !show_btn.disabled) show_btn.click();
					}
				} else if (usi_app.is_checkout_page) {
					var section = document.querySelector('[data-testid="coupon-section"]');
					if (section) {
						coupon_input = section.querySelector('[data-purpose="coupon-input"]');
						coupon_button = section.querySelector('[data-purpose="coupon-submit"]');
						if (!coupon_input) {
							var toggle_btn = section.querySelector('button');
							if (toggle_btn) toggle_btn.click();
						}
					}
				}

				if (coupon_input !== null && coupon_button !== null) {
					var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
						window.HTMLInputElement.prototype, 'value').set;
					nativeInputValueSetter.call(coupon_input, usi_app.coupon);
					coupon_input.dispatchEvent(new Event('input', { bubbles: true }));
					coupon_input.dispatchEvent(new Event('change', { bubbles: true }));
					coupon_button.click();
					usi_cookies.set("usi_coupon_applied", usi_app.coupon, usi_cookies.expire_time.week);
					usi_cookies.del("usi_coupon");
					usi_app.coupon = "";
					usi_commons.log("Coupon applied");
				} else {
					if (usi_app.coupon_attempts == undefined) {
						usi_app.coupon_attempts = 0;
					} else if (usi_app.coupon_attempts >= 5) {
						//usi_commons.report_error("Coupon elements not found");
						return;
					}
					usi_app.coupon_attempts++;
					usi_commons.log("Coupon elements missing, trying again. Tries: " + usi_app.coupon_attempts);
					setTimeout(usi_app.apply_coupon, 1000);
				}
			} catch(err) {
				usi_commons.report_error(err);
			}
		};
		
		
		usi_app.start_pdp_monitor = function(){
			try {
				usi_commons.log("usi_app.start_pdp_monitor()");
				usi_app.monitor_pdp = function() {
					try {
						if (usi_app.is_pdp_page) {
							var product = usi_app.scrape_pdp();
							if (product && product.name && product.pid) {
								//var stored_pid = usi_cookies.get("usi_prod_pid_1");//stored_pid !== product.pid ||
								if (JSON.stringify(usi_app.current_product) !== JSON.stringify(product)) {
									usi_app.current_product = product;
									usi_app.save_cart(product);
									usi_app.load();
								}
							}
						}
						return setTimeout(usi_app.monitor_pdp, 1000);
					} catch(err) {
						usi_commons.report_error(err);
					}
				};
				if (!usi_app.pdp_timeout) {
					usi_app.pdp_timeout = usi_app.monitor_pdp();
				}
			} catch(err) {
				usi_commons.report_error(err);
			}
		};
		
		usi_app.save_cart = function(product){
			try {
				usi_commons.log("usi_app.save_cart()");
				var cart_prefix = "usi_prod_";
				usi_cookies.flush("usi_subtotal");
				usi_cookies.flush(cart_prefix);

				if (product && product.pid) {
					usi_commons.log(product);
					usi_cookies.set("usi_subtotal", product.price || "", usi_cookies.expire_time.week);
					usi_cookies.set("usi_pids", product.pid, usi_cookies.expire_time.week);
					for (var prop in product) {
						if (product.hasOwnProperty(prop)) {
							usi_cookies.set(cart_prefix + prop + "_1", product[prop], usi_cookies.expire_time.week);
						}
					}
				}
			} catch(err) {
				usi_commons.report_error(err);
			}
		};
		usi_app.scrape_subtotal = function() {
			try {
				var sf = document.querySelector('[data-purpose="subscription-sticky-footer"]');
				var sp = sf ? sf.textContent.split('$') : [];
				if (sp[1]) return sp[1].split(' ')[0];
			} catch (err) {
				usi_commons.report_error(err);
			}
		};
		usi_app.scrape_pdp = function() {
			try {
				var product = {};
				var h1 = document.querySelector('h1');
				product.name = h1 ? h1.textContent.trim() : "";

				var img = document.querySelector('[aria-label="Play course preview"] img');
				if (img == null) {
					img = document.querySelector("div[class^='course-preview-entry-point-module-scss-module'] img")
				}
				var imgSrc = img ? img.src : "";
				var idMatch = imgSrc.match(/\/course\/[^\/]+\/(\d+_[^.?]+)/);
				var imgFile = idMatch ? idMatch[1] : "";
				product.pid = imgFile ? imgFile.split('_')[0] : "";
				product.image = imgFile ? "https://img-c.udemycdn.com/course/200_H/" + imgFile + ".jpg" : "";

				product.link = location.href;

				if (document.querySelector('[data-purpose="subscription-sticky-footer"]') != null) {
					var sf = document.querySelector('[data-purpose="subscription-sticky-footer"]');
					var sp = sf ? sf.textContent.split('$') : [];
					product.price = sp[1] ? sp[1].split(' ')[0] : "";
				} else if (document.querySelector("span[class^='_title-price_']") != null) {
					product.price =  document.querySelector("span[class^='_title-price_']").textContent.replace('$', '').trim()
				} else {
					var sf = document.querySelector('[class*="sticky-footer"]');
					var priceText = sf ? sf.textContent : "";
					var priceMatch = priceText.match(/$([\d.]+)/);
					product.price = priceMatch ? priceMatch[1] : "";
				}

				var instructorLinks = document.querySelectorAll('a[href*="/user/"]');
				var instructors = [];
				for (var i = 0; i < instructorLinks.length && i < 3; i++) {
					var name = instructorLinks[i].textContent.trim();
					if (name && instructors.indexOf(name) === -1) instructors.push(name);
				}
				product.instructors = instructors.join(", ");

				var srRating = document.querySelector('[class*="star-wrapper"] .ud-sr-only');
				var ratingMatch = srRating ? srRating.textContent.match(/Rating:\s*([\d.]+)/) : null;
				product.rating = ratingMatch ? ratingMatch[1] : "";

				var ratingCountEl = document.querySelector('[class*="ratings-text"] .ud-btn-label');
				var rcMatch = ratingCountEl ? ratingCountEl.textContent.match(/([\d,]+)\s*ratings/) : null;
				product.rating_count = rcMatch ? rcMatch[1] : "";

				var statsEl = document.querySelector('[data-testid="curriculum-stats"]');
				var statsText = statsEl ? statsEl.textContent : "";
				var hoursMatch = statsText.match(/([\d.]+h?\s*[\d]*m?)\s*total/i);
				product.hours = hoursMatch ? hoursMatch[1].trim() : "";
				var lecturesMatch = statsText.match(/([\d,]+)\s*lectures/i);
				product.lectures = lecturesMatch ? lecturesMatch[1] : "";
				product.level = "All Levels";

				var ribbons = usi_dom.get_elements('[class*="ribbon"] [class*="ribbon"]');
				product.bestseller = "false";
				product.premium = "false";
				for (var r = 0; r < ribbons.length; r++) {
					var text = ribbons[r].textContent.trim();
					if (text === "Bestseller") product.bestseller = "true";
					if (text === "Premium") product.premium = "true";
				}
				if (product.premium === "false") {
					var badges = document.querySelectorAll('[class*="badge"]');
					for (var b = 0; b < badges.length; b++) {
						if (badges[b].textContent.trim() === "Premium") {
							product.premium = "true";
							break;
						}
					}
				}

				return product;
			} catch (err) {
				usi_commons.report_error(err);
			}
		};
		usi_app.check_for_change = function(){
			if (usi_app.current_page == undefined || usi_app.current_page != location.href) {
				usi_app.current_page = location.href;
				usi_dom.ready(function(){
					try {
						usi_app.main();
					} catch (err) {
						usi_commons.report_error(err);
					}
				});
				usi_commons.log("USI: running main");
			}
			setTimeout(usi_app.check_for_change, 1000);
		};
		if (!usi_app.check_for_change_timeout_id) {
			usi_app.check_for_change_timeout_id = setTimeout(usi_app.check_for_change, 1000);
		}
	} catch(err) {
		usi_commons.report_error(err);
	}
}
