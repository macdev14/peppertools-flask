import React, { useState, useEffect } from 'react';
//import ReactDOM from 'react-dom';
//import Button from '@material-ui/core/Button';
import { DataGrid } from '@material-ui/data-grid';
import axios from 'axios'

export default class Table extends React.Component
{


    constructor(props){
        super(props);
        this.state = {
            processos : [],
            production : []
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
   
    let arr = [...this.state.processos, {field : val['Nome'], width: 180}]
    this.setState({processos: arr})
    
     
   })
   this.requestOS()
 
})
  }


 requestOSstatus(nOs, index){
     
     let response = axios.get(`https://peppertools.herokuapp.com/api/progress/${nOs}`, {headers: {'authorization': localStorage.getItem('auth') }}).then((response) =>{ return response.data
     }).then((res)=>
     { 
      //let index = ( this.state.processos.findIndex(x => x.field  === res[0]['Nome']) ) + 1
      //console.log(index) 
      let arr = [...this.state.production, {id: index, [res[0]['Nome']] : nOs.toString()}]
      this.setState({production: arr})
     }
     )
     
  // console.log(response.data)
   /*response.data.map((val, i) => {
   
    let arr = [...this.state.processos, {field : val['Nome'], width: 200}]
    this.setState({processos: arr})
    console.log(arr)*
    
     */
   
   
 

 }

 

    componentDidMount(){
     this.requestProcesses()
        
    }
        
   

        

    render(){
        var that = this;
        console.log(that.state.production);
        return(
         <div style={{ height: 500, width: '100%', color: '#000000', display: 'flex', justifyContent:'center', alignItems:'center' }}>
       <DataGrid
  columns={that.state.processos}
  rows={that.state.production} components={{
    Toolbar: CustomToolbar,
  }} />
       
        </div>
        )
        
        }
}