  function deletar(id){
    return(
        document.getElementById('alerts').innerHTML += 
        `
     <div class="modal fade" id="confirmar${id}" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Confirmar Exclusão</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <a href="delete/table={{table}}&id=${id}">
        <button type="button" class="btn btn-primary">Deletar</button></a>
      </div>
    </div>
  </div>
</div>`)}