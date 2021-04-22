
  $('#data').mask('00/00/0000');
  $('#vencimento').mask('00/00/0000');
  $('#data_pagamento').mask('00/00/0000');
  $('#cep').mask('00000-000');

if (document.getElementsByClassName('add-input') && typeof document.getElementsByClassName('add-input') !== 'undefined'){

  $(document).ready(function(){
    var max_input_fields = 10;
    var add_input = $('.add-input');
    var form_group = $('.form-group');
    var new_input = '<div><input type="text" name="item[]" value=""/><a href="javascript:void(0);" class="remove-input" title="Remove input"><i class=""></i></a></div>';
    var add_input_count = 1; 
    $(add_input).click(function(){
        if(add_input_count < max_input_fields){
            add_input_count++; 
            $(form_group).append(new_input); 
        }
    });
    $(form_group).on('click', '.remove-input', function(e){
        e.preventDefault();
        $(this).parent('div').remove();
        add_input_count--;
    });
});

}


if (document.getElementById('numero_nf-label') && typeof document.getElementById('numero_nf-label').innerHTML != 'undefined' ) {
  document.getElementById('numero_nf-label').innerHTML = 'Número N.F';
  document.getElementById('data_nf-label').innerHTML = 'Data da N.F';
  document.getElementById('valor_nf-label').innerHTML = 'Valor da N.F';
  document.getElementById('data_nf').placeholder = 'dd/mm/yyyy';

}

if (document.getElementById('id_cliente-label') && typeof document.getElementById('id_cliente-label').innerHTML != 'undefined' ) {
   document.getElementById('id_cliente-label').innerHTML = 'Cliente';
}

if (document.getElementById('cod_func-label') && typeof document.getElementById('cod_func-label').innerHTML != 'undefined' ) {
   document.getElementById('cod_func-label').innerHTML = 'Colaborador';
}

if (document.getElementById('codigo-label') && typeof document.getElementById('codigo-label').innerHTML != 'undefined') {
   document.getElementById('codigo-label').innerHTML = 'Código';
  document.getElementById('cod_mat-label').innerHTML = 'Material';
   document.getElementById('descricao').addEventListener('input',  async function(evt){
    
    if (document.getElementById("codigo").value == '' || document.getElementById("codigo").value=='None'){
          var word = '';
          var number = Math.floor(Math.random() * 90 + 10)
          var words = this.value.split(" ");
          for(var i = 0; i< words.length-1; i++)
          {
              word += words[i][0]
          }
           console.log(word)
           
          document.getElementById("codigo").value = word + number

    }
          

    
   
  
})
   
}

if (document.getElementById('descricao-label') && typeof document.getElementById('descricao-label').innerHTML != 'undefined' &&
  document.getElementById('cod_item-label') && typeof document.getElementById('cod_item-label').innerHTML != 'undefined') {
   document.getElementById('cod_item-label').innerHTML = 'Item';
   document.getElementById('descricao').addEventListener('input',  async function(evt){
    
    if (document.getElementById("cod_item").value == '' || document.getElementById("cod_item").value=='None'){
          var word = '';
          var number = Math.floor(Math.random() * 90 + 10)
          var words = this.value.split(" ");
          for(var i = 0; i< words.length-1; i++)
          {
              word += words[i][0]
          }
           console.log(word)
          document.getElementById("cod_item").value = word + number

    }
  } )
}




if (document.getElementById('cod_for-label') && typeof document.getElementById('cod_for-label').innerHTML != 'undefined' ) {
    document.getElementById('cod_for-label').innerHTML = 'Código Fornecedor';
    document.getElementById('cod_for').placeholder = 'Insira o Código do Fornecedor';
}

if (document.getElementById('cod_cli-label') && typeof document.getElementById('cod_for-label').innerHTML != 'undefined' ) {
    document.getElementById('cod_cli-label').innerHTML = 'Código do Cliente';
    document.getElementById('cod_cli').placeholder = 'Insira o Código do Cliente';
}

if (document.getElementById('qntcompras-label') && typeof document.getElementById('qntcompras-label').innerHTML != 'undefined' ) {
    document.getElementById('qntcompras-label').innerHTML = 'Quantidade de Compras';
    document.getElementById('qntcompras').placeholder = 'Insira a Quantidade de Compras (Opcional)';
    document.getElementById("qntcompras").required = false;
    document.getElementById("qntcompras").type = 'number';
    $("#qntcompras").attr({
      "min" : 0
    });
}

if (document.getElementById('ie-label') && typeof document.getElementById('ie-label').innerHTML != 'undefined' ) {
    document.getElementById('ie-label').innerHTML = 'Inscrição Estadual';
    document.getElementById('ie').placeholder = 'Insira a Inscrição Estadual';
    document.getElementById("ie").required = false;
}

if (document.getElementById('fax-label') && typeof document.getElementById('fax-label').innerHTML != 'undefined' ) {
    document.getElementById('fax-label').innerHTML = 'Celular';
    document.getElementById('fax').placeholder = 'Celular (Opcional)';
    document.getElementById("fax").required = false;
}


if (document.getElementById('celular-label') && typeof document.getElementById('celular-label').innerHTML != 'undefined' ) {
    document.getElementById('celular-label').innerHTML = 'Celular';
    document.getElementById('celular').placeholder = 'Celular (Opcional)';
    document.getElementById("celular").required = false;
}

if (document.getElementById('obs-label') && typeof document.getElementById('obs-label').innerHTML != 'undefined' ) {
    document.getElementById("obs").required = false;
    document.getElementById('obs-label').innerHTML = 'Observação';
    document.getElementById('obs').placeholder = 'Insira Observação (Opcional)';
}

if (document.getElementById('cnpj-label') && typeof document.getElementById('cnpj-label').innerHTML != 'undefined' ) {
    document.getElementById('cnpj-label').innerHTML = 'CNPJ';
    document.getElementById('cnpj').placeholder = 'Insira CNPJ';
}

if (document.getElementById('endereco-label') && typeof document.getElementById('endereco-label').innerHTML != 'undefined' ) {
    document.getElementById('endereco-label').innerHTML = 'Endereço';
    document.getElementById('endereco').placeholder = 'Insira o Endereço';
}

if (document.getElementById('cep-label') && typeof document.getElementById('cep-label').innerHTML != 'undefined' ) {
    document.getElementById('cep-label').innerHTML = 'CEP';
    document.getElementById('cep').placeholder = 'Insira o CEP';
}


if (document.getElementById('qt-label') && typeof document.getElementById('qt-label').innerHTML != 'undefined' ) {
  document.getElementById('qt-label').innerHTML = 'Quantidade';
  document.getElementById('mm-label').innerHTML = 'Milimetros';
  $('#cep').mask('00000-000');
  document.getElementById("data").attributes["required"] =  "";  
  document.getElementById('gaveta').type = 'number';
  document.getElementById('qt').type = 'number';
  document.getElementById('qt').placeholder = 'Insira a Quantidade';
}
if ( document.getElementById('cod_pc') && typeof document.getElementById('cod_pc').innerHTML != 'undefined'){
  document.getElementById('cod_pc-label').innerHTML = 'Código da Peça';
  document.getElementById('cod_pc').placeholder = 'Insira o Código da Peça';
  document.getElementById('id_cliente-label').innerHTML = 'Cliente';
  document.getElementById('mm').type = 'number';
}
if (document.getElementById('prazo_entrega-label') && typeof document.getElementById('prazo_entrega-label').innerHTML != 'undefined'){
  document.getElementById('prazo_entrega-label').innerHTML = 'Prazo de Entrega';
  document.getElementById('prazo_entrega').placeholder = 'Prazo de Entrega';

  document.getElementById('prazo_pagto-label').innerHTML = 'Prazo de Pagamento';
  document.getElementById('prazo_pagto').placeholder = 'Insira o Prazo de Pagamento';

  if (document.getElementById('cod_item-label') && typeof document.getElementById('cod_item-label').innerHTML != 'undefined'){
     document.getElementById('cod_item-label').innerHTML = 'Item';}
  

  //document.getElementById('prazo_entrega-label').innerHTML = 'Prazo de Entrega';
  

}

if ( document.getElementById('cnpj') && typeof document.getElementById('cnpj').innerHTML != 'undefined'){
  
  cnpj = document.getElementById('cnpj')
  cnpj.addEventListener('input', async function(evt){
    
    await loadcnpj(this.value)});
  
}

if ( document.getElementById('data_pagamento-label') && typeof document.getElementById('data_pagamento-label').innerHTML != 'undefined'){
  document.getElementById('cod_fornecedor-label').innerHTML = 'Fornecedor';
  //document.getElementById('emptyoption').innerHTML = 'Fornecedor'
  document.getElementById('vencimento').placeholder = 'dd/mm/yyyy';
  document.getElementById('data_pagamento-label').innerHTML = 'Data do Pagamento';
  document.getElementById('data_pagamento').placeholder = 'dd/mm/yyyy';
  $('#valor').mask("# ##0,00", {reverse: true});
  $('#pago').mask("# ##0,00", {reverse: true});
  $('#vencimento').mask("00/00/0000");
  $('#data_pagamento').mask("00/00/0000");
}













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
        if (typeof document.getElementById("cod_cli") !== 'undefined' && document.getElementById("cod_cli")){
        if (document.getElementById("cod_cli").value == '' || document.getElementById("cod_cli").value=='None'){
          var number = Math.floor(Math.random() * 90 + 10)
          var word = '';
          var words = response.data.name.split(" ");
          for(var i = 0; i< words.length-1; i++)
          {
              word += words[i][0]
          }
           console.log(word)
       
        
             document.getElementById("cod_cli").value = word + '01'
           }
          }
        if  (typeof document.getElementById("cod_for") !== 'undefined' && document.getElementById("cod_for")) {
        if (document.getElementById("cod_for").value == '' || document.getElementById("cod_for").value=='None'){
        
          {
          var word = '';
          var words = response.data.name.split(" ");
          for(var i = 0; i< words.length-1; i++)
          {
              word += words[i][0]
          }
          console.log(word)
            document.getElementById("cod_for").value = word + number
          }
        }
      }
    } else {
      document.getElementById("nome").value = response.data.message;
    }
  });
}

