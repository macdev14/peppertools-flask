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
  const URL = `http://www.whateverorigin.org/get?url=https://www.receitaws.com.br/v1/cnpj/${cnpj.toString().replace(/[\. ,:-]+/g, "")}`;
  await axios(URL, { headers : {
    "Access-Control-Allow-Origin" : "*",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
   
  }}).then((response) => {
    console.log(response)
     
    if (response.status == 200 && response.statusText == "OK") {
      document.getElementById("nome").value = response.data.nome;
      document.getElementById("endereco").value = response.data.logradouro;
      document.getElementById("cidade").value = response.data.municipio;
      document.getElementById("estado").value = response.data.uf;
      document.getElementById("cep").value = response.data.cep.replace(/\D/g, "");
      document.getElementById("email").value = response.data.email;
    } else {
      document.getElementById("nome").value = response.data.message;
    }
  });
}

