import React from "react";
import ReactDOM from "react-dom";
import Table from "./Table";
import Textselect from "./dynamicOption"
import Scanner from "./scanner";
if (document.getElementById("app") && typeof document.getElementById("app") !== 'undefined'){

ReactDOM.render(<Table/>, document.getElementById("app"));

}

if (document.getElementById("optdiv")  && typeof document.getElementById("optdiv") !== 'undefined'){
    ReactDOM.render(<Textselect/>, document.getElementById("optdiv"));
}

if (document.getElementById("scanner")  && typeof document.getElementById("scanner") !== 'undefined'){
    ReactDOM.render(<Scanner/>, document.getElementById("scanner"));
}