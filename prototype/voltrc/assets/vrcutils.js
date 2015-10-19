
var REST_URL = 'WEBRC';
//var selectedDb = null;

function getREST(method,request, indata, proc,failproc, ip) {

  var fullurl = REST_URL + "?request=" + encodeURIComponent(request) + "&method=" 
		+ encodeURIComponent(method) + "&data=" + encodeURIComponent(indata);
  if (ip != "") fullurl = "http://" + ip + "/" + fullurl;

  ADD_DEBUG("REST URL: " + fullurl);

            $.ajax(
                {
         	   type: method,
                   url: fullurl,
                   jquerycrossDomain: true,
                   contentType: "application/json",  //; charset=utf-8",
                   dataType: "jsonp",
                   success: function(data) { proc(data); },               
                   error: function(msg,text,err) { failproc (msg, text, err); }
                 });



}

function goodREST(data) {

 //ADD_DEBUG("Success! " + JSON.stringify(data,null,2));
 //var jobj = jQuery.parseJSON( data );
ADD_DEBUG(JSON.stringify(data));
 

}
function badREST(A,B,C) {

  ADD_DEBUG("Failed!" + 'msg = ' +  JSON.stringify(A) + ', Status = ' + B + ', ErrorThrown = ' + JSON.stringify(C));
        
}

function dorestcall() {
var method = document.getElementById("RESTmethod").value;
var request = document.getElementById("RESTrequest").value;
var indata = document.getElementById("RESTdata").value;

getREST(method, request, indata, goodREST, badREST);

}

function htmlEncode(value){
    if (value) {
        return jQuery('<div />').text(value).html();
    } else {
        return '';
    }
}
 
function htmlDecode(value) {
    if (value) {
        return $('<div />').html(value).text();
    } else {
        return '';
    }
}


