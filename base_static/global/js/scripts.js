function my_scope() {
    //Busca todos os forms que possuem a classe 'form-delete'
    const forms = document.querySelectorAll('.form-delete');
  
    //Fazemos um for para pegar cada um deles (Se tiver mais de um)
    //E adicionamos um evento extra após o submit do form (Os dados serem enviados)
    for (const form of forms) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        
        //Criamos uma janela de confirmação
        const confirmed = confirm('Você tem certeza');
  
        //Apenas se confirmado for verdadeiro, ele envia os dados do form
        if (confirmed) {
          form.submit();
        }
      });
    }
  }
  
  my_scope();