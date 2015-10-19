/*
function initUI() {
  getREST("GET","databases","",refresh_db, badREST);

}
*/
function refresh_db(data) {
  // ADD_DEBUG("refreshing databases!");
   // Announce it
   goodREST(data);

   //deal with it.
   outstr = ""
 //  ADD_DEBUG ("DB list length: " + data.Databases.length);
   for (var db in data.Databases) {
      outstr +=  "<p>Database: " + htmlEncode(JSON.stringify(data.Databases[db])) + "</p>";
   //ADD_DEBUG ("DB  length: " + data.Databases[db].length)
      outstr +=  "<p>Database inner: " + htmlEncode(JSON.stringify(data.Databases[db].Database)) + "</p>";
  // ADD_DEBUG ("Collect info..");
   var d = data.Databases[db].Database
   UiAddDatabase(d);     
     
   }

   // Remove deleted databases
  UiTrimDbList(data.Databases);

  ADD_DEBUG(outstr);

   // Pick a database
  if (!getActiveDb()) { ADD_DEBUG("Pick a DB!"); makeActiveDb(null); }
  refresh_config();

}

function updateConfigDb(data) {
   // Announce it
   goodREST(data);
	ADD_DEBUG("Got database!");
	// Set title etc.
	var title = "<b>" + htmlEncode(data.Database["name"]) + '</b><br/><span style="font-size:x-small;">Status: ' + data.Database.status +"</span>";
	var dbmain = document.getElementById("DBMainEntity");
 	dbmain.innerHTML = title;
	dbmain.className = data.Database.status.toLowerCase();
	// Add servers
	for (s in data.Database.Servers) {
		ADD_DEBUG("Adding a Server...");
		UiAddServer(data.Database.Servers[s]);
	}
		ADD_DEBUG("Trim Server list...");
 	UiTrimServerList(data.Database.Servers);
	// Set parameters
	var output = ""
	for (o in data.Database) {
		  var settable = "";
		  if (dbMap.hasOwnProperty(o)) {
		     settable = "\nSet " + dbMap[o].id + " = " + JSON.stringify(data.Database[o]);
		 
		    document.getElementById(dbMap[o].id).value = data.Database[o];
		  }

		    output += "\n\nkey: " + o + " object: " + JSON.stringify(data.Database[o]) + settable;
	}
	ADD_DEBUG(output);
}


function refresh_config() {
  ADD_DEBUG("Refresh db!");
  if (!getActiveDb()) { 
	// No database selected
	// hide config, show message
	ADD_DEBUG ("No database selected");
	return;
  }
  var dbId = getActiveDb().id.substring(2);
	ADD_DEBUG("go rest it up....");
  var db = getREST("GET","databases/" + dbId,"",updateConfigDb, badREST)
}

function UiTrimDbList(VemList) {
   var dblist = document.getElementById("databases");
   var currentlist = dblist.childNodes;
   var cid;
   for (var i=0; i<currentlist.length; i++) {
      if (!currentlist[i].id) {
          cid = "donotdelete";
 	  //ADD_DEBUG("No ID: " + JSON.stringify(currentlist[i]));
      } else {
          cid = currentlist[i].id.substring(2);
      }
      found = false;
      for (var db in VemList) {
          if (VemList[db].Database.id == cid ) found = true;
      }
      if (!found && cid != "donotdelete") dblist.removeChild(currentlist[i]); 
  }
   

}
function makeActiveDb(obj) {
  var currentselection = null;
	// Deselect any that are currently active
  var clist = document.getElementById("databases").childNodes;
  for (var i=0;i<clist.length;i++) {
     var cname = clist[i].className;
     if (cname && cname != "") {
        if (cname.indexOf("active") >=0) { ADD_DEBUG("Found current selection..."); currentselection = clist[i]; }
        cname = cname.replace("active","");
        cname = cname.replace("  "," ");
        clist[i].className = cname;
     };
  }
	// If none specified, make the first one active
  if (!obj) {
     if (!currentselection) {
             ADD_DEBUG("Nothing specified, nothing selected...");
	     var i = 0;
	     while (!obj && i< clist.length) {
		var id = clist[i].id;
		if (id) { if (id.substring(0,2) == "DB") obj = clist[i]; };
		i++;
	     }
     } else {
	obj = currentselection;
     }
  }
  if (obj) { ADD_DEBUG ("Make it active!"); obj.className += " active"; }

}

function getActiveDb() {
  var clist = document.getElementById("databases").childNodes;
  for (var i=0;i<clist.length;i++) {
     var cname = clist[i].className;
     if (cname && cname != "") {
        if (cname.indexOf("active") >=0) { return(clist[i]); }
     };
  }
  return (null);

}

function UiAddDatabase(db) {
   var dblist = document.getElementById("databases");
   var currentlist = dblist.childNodes;
   var otext = "<b>" + db.name + '</b><br/><span style="font-size:x-small;">ID: ' + db.id + "<br/>Status: " + db.status +"</span>";
   var li = null;
   var isnew = true;
   dbg = "";
   for (var i=0; i<currentlist.length; i++) {
      dbg += "\nChecking " + db.id  + " with " + currentlist[i].id;
      if (currentlist[i].id == "DB" + db.id) {
      	li = currentlist[i];
	isnew = false;
        dbg += "Found a match!";
      }
   }
   if (li == null) {
	li = document.createElement("li");
   	li.innerHTML = otext;
   	li.id = "DB" + db.id;
   	li.className = "db " + db.status.toLowerCase();
	li.addEventListener("click", selectDb, false);
    } else {
	if (li.className.indexOf("active") > 0) {
		li.className = "db " + db.status.toLowerCase() + " active";
        } else {
		li.className = "db " + db.status.toLowerCase();
	}
    }
    //ADD_DEBUG(dbg);
    if (isnew) dblist.appendChild(li);

}

function UiAddServer(server) {
   var dblist = document.getElementById("servers");
   var currentlist = dblist.childNodes;
   var otext = "<b>" + server.name + '</b><br/><span style="font-size:x-small;">ID: ' + server.server + "<br/>Status: " + server.status +"</span>";
   var li = null;
   var isnew = true;
   dbg = "";
   for (var i=0; i<currentlist.length; i++) {
      dbg += "\nChecking " + server.server  + " with " + currentlist[i].id;
      if (currentlist[i].id == "SV" + server.server) {
      	li = currentlist[i];
	isnew = false;
        dbg += "Found a match!";
      }
   }
   if (li == null) {
	li = document.createElement("div");
   	li.innerHTML = otext;
   	li.id = "SV" + server.server;
   	li.className = "server " + server.status.toLowerCase();
	//li.addEventListener("click", selectServer, false);
    }
    //ADD_DEBUG(dbg);
    if (isnew) dblist.appendChild(li);

}

function UiTrimServerList(VemList) {
   var serverlist = document.getElementById("servers");
   var currentlist = serverlist.childNodes;
   var cid;
   for (var i=0; i<currentlist.length; i++) {
      if (!currentlist[i].id) {
          cid = "donotdelete";
 	  //ADD_DEBUG("No ID: " + JSON.stringify(currentlist[i]));
      } else {
          cid = currentlist[i].id.substring(2);
      }
      found = false;
      for (var server in VemList) {
          if (VemList[server].server == cid ) found = true;
      }
      if (!found && cid != "donotdelete") serverlist.removeChild(currentlist[i]); 
  }
   

}

/*  BUTTON RESPONSES */

function selectDb() {
   var obj = this;
   makeActiveDb(obj);
   refresh_config();
}



