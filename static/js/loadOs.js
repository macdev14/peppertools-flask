document.addEventListener("DOMContentLoaded", function (event) {
  if (parseInt(document.getElementById("Id_Cliente")) <= 0) {
    getElementById("msg").innerHTML = "Selecione um cliente válido";
    document.getElementById("cad").disabled = true;
  }
});

async function loadOs(limit = 10) {
  document.getElementById("all").innerHTML = "";

  const URL = `https://peppertools.cf/api/os/limit=${limit.toString()}`;
  await axios(URL).then((response) => {
    console.log(response);
    response.data.map((val, i) => {
      console.log(val);
      document.getElementById("all").innerHTML += `<tr> 
      <th scope="row"><a href='/os/form/print/${val.Id}' target='_blank'> ${
        val.Numero_Os
      } </a></th>
      <td>${val.nome.replace(/\s.*/, "")}</td>
      <td>${val.Data}</td>
      <td>${val.Prazo}</td>
      <td>${val.Especificacao}</td>
       <td width="15%" float="left"><a href="os/form/${val.Id}">
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="os/form/delete/${val.Id}">
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
    </tr>
    `;
    });
  });
}

async function filterOs(q) {
  document.getElementById("all").innerHTML = "<p>Carregando..</p>";
  let limit = document.getElementById("limit").value;
  //let q = document.getElementById("query").value;
  console.log(q);
  if (!limit) {
    limit = 10;
  }
  const URL = `https://peppertools.cf/api/os/q=${q.toString()}`;
  document.getElementById("all").innerHTML = "";
  await axios(URL).then((response) => {
    response.data.map((val, i) => {
      console.log(val);
      document.getElementById("all").innerHTML += `<tr> 
      <th scope="row"><a href='/os/form/print/${val.Id}' target='_blank'> ${val.Numero_Os} </a></th>
      <td>${val.nome}</td>
      <td>${val.Data}</td>
      <td>${val.Prazo}</td>
      <td>${val.Especificacao}</td>
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
    `;
    });
  });
}

document.addEventListener("DOMContentLoaded", loadOs(10));
//document.getElementById("query").addEventListener('change', filterOs());
