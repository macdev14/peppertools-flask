import React, { useState, useEffect } from 'react';
//import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { DataGrid, ptBR } from '@material-ui/data-grid';
import axios from 'axios'
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
const parse = require('html-react-parser');
export default class Table extends React.Component
{


    constructor(props){
        super(props);
        this.state = {
            processos : [],
            production : [],
            modalOpen: false,
            divHeight: 0
        }
    }


 requestOS(){
    return axios.get(`https://peppertools.herokuapp.com/api/progress/allos`, {headers: {'authorization': localStorage.getItem('auth') }}).then((response) => {
    response.data.map((val, i) => {
    return this.requestOSstatus(val, i)
   })
    })
 }



  requestProcesses(){
  let response = axios.get('https://peppertools.herokuapp.com/api/processos', {headers: {'authorization': localStorage.getItem('auth') }}).then((response) => {
  // console.log(response.data)
   response.data.map((val, i) => {
   
    let arr = [...this.state.processos, {field : val['Nome'], flex: 1, headerAlign: 'center', 
    renderCell: (params) => {
            console.log(params)
            console.log(val['Nome'])
            let col = '#info'+ params.row.id.toString()
            return( <a href="#" data-toggle="modal" class="cell-info" color="#000000" data-target={col}> {params.row[params.field]}</a>)
    }
    
     } ]
    this.setState({processos: arr})
    
     
   })
   this.requestOS()
 
})
  }


 requestOSstatus(nOs, index){
     
     let response = axios.get(`https://peppertools.herokuapp.com/api/progress/${nOs}`, {headers: {'authorization': localStorage.getItem('auth') }}).then((response) =>{ return response.data
     }).then((res)=>
     { 
      let modal = nOs.toString() + ' - '+ res[0]['nome'].substring(0, 6) + "- " + res[0]['Tipo'].substring(0, 3).toUpperCase()
      let arr = [...this.state.production, {id: res[0]['ID'], [res[0]['Nome']] : modal} ]
      this.setState({production: arr})
     }
     )   

 }

 

    componentDidMount(){
     this.requestProcesses()
        
    }
        
  theme = createMuiTheme({
    palette: {
        primary: { main: '#ffffff' },
    },
    }, ptBR);

        

    render(){
        var that = this;
        console.log('state')
        console.log(that.state.production)
        return(
         <div style={{ height: 400, width: '100%', color: '#000000', display: 'flex', justifyContent:'center', alignItems:'center' }}>
       <ThemeProvider theme={that.theme}>
       <DataGrid apiRef={that.requestProcesses} columns={that.state.processos} rows={that.state.production} />
       </ThemeProvider>;
        </div>
        )
        
        }
}