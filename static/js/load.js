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
  const URL = `https://api.cnpja.com.br/companies/${cnpj.toString().replace(/[\. ,:-]+/g, "").replace('/', "")}`;
  await axios(URL, { headers : {
    "authorization" : "481d9c30-5b4e-4eaf-a654-5eb36712c539-d259ade5-2992-4b43-a97d-ac2ccc4b481d"
   
  }}).then((response) => { 
    if (response.status == 200) {
      if (document.getElementById("nome").value == '' || document.getElementById("nome").value=='None')
      {
          document.getElementById("nome").value = response.data.name;
      }
      if (document.getElementById("cidade").value == '' || document.getElementById("cidade").value=='None'){
        document.getElementById("cidade").value = response.data.address.city;
      }
      if (document.getElementById("estado").value == '' || document.getElementById("estado").value=='None'){
         document.getElementById("estado").value = response.data.address.state;
      }
     if (document.getElementById("cep").value == '' || document.getElementById("cep").value=='None'){
      document.getElementById("cep").value = response.data.address.zip.replace(/\D/g, "").replace(".","").replace("-","");
     }
     if (document.getElementById("email").value == '' || document.getElementById("email").value=='None'){
        if (typeof response.data.email !== 'undefined'){
          document.getElementById("email").value = response.data.email;
        }else{document.getElementById("email").value ="";}
     }
    if (document.getElementById("endereco").value == '' || document.getElementById("endereco").value=='None'){
      if (typeof response.data.address.number !== 'undefined'){
         document.getElementById("endereco").value = response.data.address.street + " " + response.data.address.number;
      }else{
         document.getElementById("endereco").value = response.data.address.street;
      }
    }
      //var counter = 0
      /*response.data.name.replace(/(\b+)/g,function (a) {
      // for each word found increase the counter value by 1
      counter++;
      })*/
      if (document.getElementById("cod_cli").value == '' || document.getElementById("cod_cli").value=='None'){
        var word = '';
        var words = response.data.name.split(" ");
        for(var i = 0; i< words.length-1; i++)
        {
            word += words[i][0]
        }
        console.log(word)
        document.getElementById("cod_cli").value = word + '01'
      }

    } else {
      document.getElementById("nome").value = response.data.message;
    }
  });
}

