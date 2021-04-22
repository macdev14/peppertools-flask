import React, { useState, useEffect } from 'react';
//import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';
import { DataGrid, ptBR } from '@material-ui/data-grid';
import axios from 'axios'
import { createMuiTheme, makeStyles, ThemeProvider } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

const parse = require('html-react-parser');
export default class Table extends React.Component
{


    constructor(props){
        super(props);
        this.state = {
            processos : [],
            production : [],
            modalOpen: false,
            divHeight: 0,
            hideNav: false,
            osProd:[],
            nRows : 0
        }
    }

   

resize() {
    let currentHideNav = (window.innerWidth <= 760);
    if (currentHideNav !== this.state.hideNav) {
        this.setState({hideNav: currentHideNav});
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
    this.setState({nRows: i})
    let arr = [...this.state.processos, {field : val['Nome'], flex: 1, headerAlign: 'center', 
    renderCell: (params) => {
            //console.log(params)
            //console.log(val['Nome'])
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
     
     let response = axios.get(`https://peppertools.herokuapp.com/api/progress/${nOs}`, {headers: {'authorization': localStorage.getItem('auth') }}).then((response) =>{ 
         let combine = [...this.state.osProd, response.data[0]];
         this.setState({osProd: combine})
         return response.data
     }).then((res)=>
     { 
      let modal = nOs.toString() + ' - '+ res[0]['nome'].substring(0, 6) + "- " + res[0]['Tipo'].substring(0, 3).toUpperCase()
      let arr = [...this.state.production, {id: res[0]['ID'], [res[0]['Nome']] : modal} ]
      this.setState({production: arr})
     }
     )   

 }

 

    componentDidMount(){
    window.addEventListener("resize", this.resize.bind(this));
    this.resize();
    this.requestProcesses()
 
    }

    componentWillUnmount() {
    window.removeEventListener("resize", this.resize.bind(this));
}
    
        
  theme = createMuiTheme({
    palette: {
        primary: { main: '#ffffff' },
    },
    }, ptBR);


    // styles

    useStyles = makeStyles({
  root: {
    minWidth: 275,
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

    // styles



    render(){
        var that = this;
        if (that.state.hideNav === true){
             //const classes = that.useStyles();
            
         
             return (
    this.state.osProd.map((val, i)=>(
         <Card style={{marginBottom: 25}}>
      <CardContent style={{ fontWeight: 400}}>
       {val['Numero_Os']} - {val['Nome']} -  {val['Tipo']}
      </CardContent>
      <CardActions>
     {val['nome']} - {val['inicio']}
      </CardActions>
    </Card>
    ))
   
  
  
  );   

        }else{
        var that = this;
        //var ht = (that.state.nRows*52) + 52
        //console.log('production')
        //console.log(that.state.production)
        return(
         <div style={{ height:750, width: '100%', color: '#000000', display: 'flex', justifyContent:'center', alignItems:'center' }}>
       <ThemeProvider theme={that.theme}>
       <DataGrid apiRef={that.requestProcesses} columns={that.state.processos} rows={that.state.production} />
       </ThemeProvider>;
        </div>
        )
        }
        }
}