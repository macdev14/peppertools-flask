

async function loadOs(limit = 10)
{ 
  document.getElementById("all_os").innerHTML = '';
  const URL = `http://localhost:5000/api/os/limit=${limit.toString()}`;
  await axios(URL).then(response =>{
      response.data.map((val, i) =>{
          console.log(val)
          document.getElementById("all_os").innerHTML += `<tr> 
      <th scope="row"><a href='/os/form/print/${val.Id}' target='_blank'> ${val.Numero_Os} </a></th>
      <td>${val.nome}</td>
      <td>${val.Data}</td>
      <td>${val.Prazo}</td>
       <td width="15%" float="left"><a href="os/form/${val.Id}" target='_blank'>
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="os/form/delete/${val.Id}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
    </tr>
    `});
  });
  
}

document.addEventListener('DOMContentLoaded', loadOs());