String.prototype.capitalize = function () {
  return this.charAt(0).toUpperCase() + this.slice(1);
};

 async function load(table, limit = 10) {
  document.getElementById("all").innerHTML = "";

  const URL = `https://peppertools.herokuapp.com/api/${table}/limit=${limit.toString()}`;
  let keys = [];
  await axios(URL,  { headers: {'authorization': localStorage.getItem('auth') } } ).then((response) => {
    keys = Object.keys(response.data[0]);
    keysId = Object.keys(response.data[0]);
    delete keys[0];
    console.log(keys);
    document.getElementById("columns").innerHTML = `<tr>`;
    keys.map((val, i) => {
      if (
        keys[i] == "id_cliente" ||
        keys[i] == "Id_Cliente" ||
        keys[i] == "cod_func" ||
        keys[i] == "cod_fornecedor"
      ) {
        keys[i] = "nome";
      }

      document.getElementById("columns").innerHTML += `<td>${keys[i]}</td>`;
    });

    response.data.map((val, i) => {
      keys.map((val2, i) => {
        document.getElementById("all").innerHTML = `<td>${val[val2]}</td>`;
      });

      document.getElementById(
        "all"
      ).innerHTML += `<td width="15%" float="left"><a href="${table}/form/${
        val[keys[0]]
      }" target='_blank'>
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="${table}/form/delete/${val[keysId]}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td> 
    
    `;
    });
  });
}

async function filter(q, table) {
  const URL = `https://peppertools.herokuapp.com/api/${table}/q=${q.toString()}`;
  document.getElementById("all").innerHTML = "";
  await axios(URL).then((response) => {
    response.data.map((val, i) => {
      document.getElementById("all").innerHTML += `
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
         <a href="${table}/form/delete/${val.ID}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
   
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

async function loadcnpj(cnpj) {
  const URL = `https://api.cnpja.com.br/companies/${cnpj.toString().replace(/[\. ,:-]+/g, "")}`;
  await axios(URL, { headers : {
    "authorization" : "481d9c30-5b4e-4eaf-a654-5eb36712c539-d259ade5-2992-4b43-a97d-ac2ccc4b481d"
   
  }}).then((response) => { 
    if (response.status == 200) {

      document.getElementById("nome").value = response.data.name;
      document.getElementById("endereco").value = response.data.address.street + " ";
      document.getElementById("cidade").value = response.data.address.city;
      document.getElementById("estado").value = response.data.address.state;
      document.getElementById("cep").value = response.data.address.zip.replace(/\D/g, "");
      if (typeof response.data.email !== 'undefined'){
        document.getElementById("email").value = response.data.email;
      }else{document.getElementById("email").value ="";}
      if (typeof response.data.address.number !== 'undefined'){
         document.getElementById("endereco").value = response.data.address.street + " " + response.data.address.number;
      }else{
         document.getElementById("endereco").value = response.data.address.street;
      }
    
    
    } else {
      document.getElementById("nome").value = response.data.message;
    }
  });
}

