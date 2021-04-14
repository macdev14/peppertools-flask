import React from "react";
import ReactDOM from "react-dom";
import Table from "./Table";
import Textselect from "./dynamicOption"
if (document.getElementById("app") && typeof document.getElementById("app") !== 'undefined'){

ReactDOM.render(<Table/>, document.getElementById("app"));

}

if (document.getElementById("optdiv")  && typeof document.getElementById("optdiv") !== 'undefined'){
    ReactDOM.render(<Textselect/>, document.getElementById("optdiv"));
}