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
            processos : []
        }
    }

  requestProcesses(){
  let response = axios.get('https://peppertools.herokuapp.com/api/processos', {headers: {'authorization': localStorage.getItem('auth') }}).then((response) => {
  // console.log(response.data)
   response.data.map((val, i) => {
   
    let arr = [...this.state.processos, {field : val['Nome'], width: 200}]
    this.setState({processos: arr})
    console.log(arr)
    
     
   })
   
 
})   
  }
    componentDidMount(){
       
     this.requestProcesses()   
        
    }
        
   

        

    render(){
        var that = this;
        return(
        <DataGrid
      columns={that.state.processos}
  rows={[
    { id: 1, name: 'React' },
    { id: 2, name: 'Material-UI' },
  ]}
    />
        )
        
        }
}