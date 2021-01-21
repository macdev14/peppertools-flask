async function loadClientes() {
  document.getElementById("all").innerHTML = "";
  const URL = `https://peppertools.herokuapp.com/api/clientes`;

  await axios(URL).then((response) => {
    response.data.map((val, i) => {
      // console.log(val)
      document.getElementById("all").innerHTML += `<tr> 
      <th scope="row">${val["cod_cli"]}</th>
      <td>${val.nome.replace(/\s.*/, "")}</td>
      <td>${val.cnpj}</td>
      <td>${val.endereco}</td>
      <td>${val.telefone}</td>
       <td width="15%" float="left"><a href="clientes/form/${
         val.ID
       }" target='_blank'>
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="clientes/form/delete/${val.ID}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
    </tr>
    `;
    });
  });
}

async function filterClient(q) {
  const URL = `https://peppertools.osc-fr1.scalingo.io/api/clientes/q=${q.toString()}`;
  document.getElementById("all").innerHTML = "";
  await axios(URL).then((response) => {
    response.data.map((val, i) => {
      document.getElementById("all").innerHTML += `<tr> 
      <th scope="row">${val["cod_cli"]}</th>
      <td>${val.nome.replace(/\s.*/, "")}</td>
      <td>${val.cnpj}</td>
      <td>${val.endereco}</td>
      <td>${val.telefone}</td>
       <td width="15%" float="left"><a href="clientes/form/${
         val.ID
       }" target='_blank'>
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="clientes/form/delete/${val.ID}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
    </tr>
    `;
    });
  });
}

function search(arr, s) {
  var matches = [],
    i,
    key;

  for (i = arr.length; i--; )
    for (key in arr[i])
      if (arr[i].hasOwnProperty(key) && arr[i][key].indexOf(s) > -1)
        matches.push(arr[i]); // <-- This can be changed to anything

  return matches;
}

document.addEventListener("DOMContentLoaded", loadClientes());
