import React, { useState, useEffect } from 'react';
import Autocomplete from '@material-ui/lab/Autocomplete'
import TextField from '@material-ui/core/TextField';
export default class dynamicOption extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            optValue : 0,
            qtdValue : 0,
            optItem: [],
            cod_mat:0,
            osID:0
        }
    }

 requestItems(){
    return axios.get(`https://peppertools.herokuapp.com/api/item/allitems`, {headers: {'authorization': localStorage.getItem('auth') }}).then((response) => {
    response.data.map((val, i) => {
    let combine = [...this.state.optItem, {descricao : val['descricao'], material:  val['nome'] } ] 
    this.setState({
        optItem : combine
    })    
    console.log(val['descricao'])
   })
    })
 }

 itemChange(id){
    return axios.post(`https://peppertools.herokuapp.com/api/item/${id}`, { descricao:optField, cod_mat: cod_mat} ,{headers: {'authorization': localStorage.getItem('auth') }}).then((response) => {
    response.data.map((val, i) => {
    console.log(val['descricao'])
   })
    })

 }

    render(){
        var that = this;
        return(
        <Autocomplete
  id="item-descricao"
  options={that.state.optItem}
  getOptionLabel={(option) => option.descricao}
  style={{ width: 300 }}
  renderInput={(params) => <TextField {...params} label="Item" variant="outlined" />}
/>
    )}
}
