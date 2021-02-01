
 
async function  progress(number){
  let el = `progress-${number}`;
  document.getElementById(el).innerHTML = "Carregando.."
  
  const URL_API = `http://localhost:5000/api/progress/${number}`
  await axios(URL_API).then((response) => {
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
            m = (100 / 4);
         if (response['data'][dict]['Nome'] != 'Finalizado')
          {
             n = n + (m/2);
          }
        else{
              n =100;
           }
           // n = m/(arr.length*4);
           document.getElementById(el).innerHTML += `<div class="progress-bar ${color}" role="progressbar" style="height:100% ;width: ${n.toString()}%" aria-valuenow="${n.toString()}" aria-valuemin="0" aria-valuemax="100"><span style="  margin: 0px auto; text-align: center;">${response['data'][dict]['inicio']} - ${response['data'][dict]['Nome']}</span></div>`
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