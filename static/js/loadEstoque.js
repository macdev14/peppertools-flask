async function loadEstoque(limit = 10) {
  document.getElementById("all").innerHTML = "";

  const URL = `https://peppertools.cf/api/estoque/limit=` + limit.toString();
  await axios(URL).then((response) => {
    response.data.map((val, i) => {
      console.log(val);
      document.getElementById("all").innerHTML += `<tr> 
      <th scope="row">${val["cod_pc"]}</th>
      <td>${val["nome"].replace(/\s.*/, "")}</td>
      <td>${val.gaveta}</td>
      <td>${val.material}</td>
      <td>${val.ferramenta}</td>
       <td width="15%" float="left"><a href="estoque/form/${
         val.ID
       }" target='_blank'>
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="estoque/form/delete/${val.ID}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
    </tr>
    `;
    });
  });
}

async function filterEstoque(q) {
  document.getElementById("all").innerHTML = "<p>Carregando..</p>";
  let col = document.getElementById("filter").value;

  // let limit = document.getElementById("limit").value;
  //let q = document.getElementById("query").value;
  console.log(q);
  if (!limit) {
    limit = 10;
  }
  const URL = `http://peppertools.herokuapp.com/api/estoque/q=${q.toString()}&col=${col.toString()}`;
  console.log(URL);
  document.getElementById("all").innerHTML = "";
  await axios(URL).then((response) => {
    response.data.map((val, i) => {
      console.log(val);
      document.getElementById("all").innerHTML += `<tr> 
      
      <td>${val.nome}</td>
      <td>${val.gaveta}</td>
      <td>${val.material}</td>
      <td>${val.ferramenta}</td>
       <td width="15%" float="left"><a href="estoque/form/${val.ID}" target='_blank'>
                <button type="submit" class="btn-link">Editar</button>
            </a>
         </td>
          <td>
         <a href="estoue/form/delete/${val.ID}" target='_blank'>
                <button type="submit" class="btn-link">Deletar</button>
            </a>
            </td>
    </tr>
    `;
    });
  });
}

document.addEventListener("DOMContentLoaded", loadEstoque());
document.getElementById("filter").addEventListener("onchange", function () {
  document.getElementById("infilter").type = "text";
});

/*
  document
  .getElementById("infilter")
  .addEventListener("onchange", filterEstoque(this.value));
*/
