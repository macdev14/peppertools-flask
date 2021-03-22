import React, { useState, useEffect } from 'react';
//import ReactDOM from 'react-dom';
//import Button from '@material-ui/core/Button';
import { DataGrid } from '@material-ui/data-grid';
import axios from 'axios'
export default function Table() {
const [processos, setProcesso] = useState('');

useEffect(()=>{


  async function requestProcesses(){
  let response = await axios.get('https://peppertools.herokuapp.com/api/processos', {headers: {'authorization': localStorage.getItem('auth') }}).then((response) => {
  // console.log(response.data)
   response.data.map((val, i) => {
   
    let arr = [...processos, {field : val['Nome']}]
    setProcesso(arr)
    console.log(arr)
    
     
   })
   console.log('Processos:')
 
})   
}

requestProcesses();

},[]
)

//useEffect(requestProcesses(), [])
  return (
    
    <DataGrid
      columns={processos}
  rows={[
    { id: 1, name: 'React' },
    { id: 2, name: 'Material-UI' },
  ]}
    />
  );
}

