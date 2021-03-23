
 
async function  progress(number){
  var isMobile = false; //initiate as false
// device detection
if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
    isMobile = true;
}
  let el = `progress-${number}`;
  document.getElementById(el).innerHTML = "Carregando.."
  
  const URL_API = `https://peppertools.herokuapp.com/api/progress/${number}`
  await axios(URL_API,  { headers: {'authorization': localStorage.getItem('auth') } } ).then((response) => {
       document.getElementById(`progress-${number}`).innerHTML = ""
       console.log(response['data'])
       
       let string = ''
       let color = ''
       let arr = []
        let m = 0 ;
       let = n = 0;
       for (dict in response['data']){
        
         console.log(dict)
         if (string === '' || dict['Nome'] != string){
         string = dict['Nome']
         }
         if (!arr.includes(response['data'][dict]['Nome'])){
              arr.push(response['data'][dict]['Nome'])
              if (isMobile){m = (100 / 2);}else{m = (100 / 4)}
            if (response['data'][dict]['Nome'] != 'Finalizado')
            {
            if (isMobile){ n = n + m;}else{ n = n + (m/2);}
            
            }
        else{
              n = 100;
           }
           // n = m/(arr.length*4);
        //   if (response['data'][dict]['fim']){
         
             document.getElementById('modals-to-open').innerHTML += `
             
              <div class="modal fade" id="info${response['data'][dict]['ID']}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                <div class="modal-header">
                  Informações
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </div>
                <div class="modal-body">
               
              ${response['data'][dict]['duration'] ? '<br>Duracao: '+ response['data'][dict]['duration'] : ''}
              ${response['data'][dict]['Tipo'] ? '<br>Tipo: '+ response['data'][dict]['Tipo'].charAt(0).toUpperCase()+ response['data'][dict]['Tipo'].slice(1) : ''}
               ${response['data'][dict]['nome'] ?   '<br>Cliente: ' + response['data'][dict]['nome'] : ''}
               ${response['data'][dict]['qtd'] ?   '<br>Quantidade: ' + response['data'][dict]['qtd'] : ''}<br>
                Processo: ${response['data'][dict]['Nome']} <br> Início:  ${response['data'][dict]['inicio']} <br> 
                ${(response['data'][dict]['fim']) ? 'Fim:' + response['data'][dict]['fim'] : 'Em andamento' }
                <br> Data: ${response['data'][dict]['data']}
                </div>
                <div class="modal-footer">
                <a href="os/form/${response['data'][dict]['ID']}">
                  <button type="button" class="btn btn-warning">Editar O.S</button></a>
                  <button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>
                  <a href="delete/table=Historico_os&id=${response['data'][dict]['ID']}">
                  <button type="button" class="btn btn-danger">Deletar</button></a>
                  </div>
                </div>
              </div>
            </div>
          </div>
             
             `
             document.getElementById(el).innerHTML += `<div class="progress-bar ${color}" data-toggle="modal" data-target="#info${response['data'][dict]['ID']}" role="progressbar" style="height:100% ;width: ${n.toString()}%" aria-valuenow="${n.toString()}" aria-valuemin="0" aria-valuemax="100"><a href="#" data-toggle="modal" data-target="#info${response['data'][dict]['ID']}"> ${response['data'][dict]['Nome']} </a> </div>`
         //  }else{
       //      document.getElementById(el).innerHTML += `<div class="progress-bar ${color}" role="progressbar" style="height:100% ;width: ${n.toString()}%" aria-valuenow="${n.toString()}" aria-valuemin="0" aria-valuemax="100"><a data-toggle="tooltip"> ${response['data'][dict]['Nome']} <span class="tooltiptext"> Início:  ${response['data'][dict]['inicio']} <br>Data: ${response['data'][dict]['data']} </span> </div> </div>`
    //       }
           
         }
         
         
       
       
     
      
       
       color = 'bg-info'
       }
    /*   for (const [key, value] of Object.entries(dict))
       {
          
       }
       }
       return(<h5 class="card-title">{{n_os}}</h5>
          
            <div class="progress">
              
              <div class="progress-bar" role="progressbar" style="width: 15%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
              <div class="progress-bar bg-success" role="progressbar" style="width: 30%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
              <div class="progress-bar bg-info" role="progressbar" style="width: 20%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
            </div>*/
         
    })
  }