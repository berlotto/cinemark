$(document).ready(function(){
	/* =========================
	   ScrollReveal
	   (on scroll fade animations)
	============================*/
	var revealConfig = { vFactor: 0.20 }
	window.sr = new scrollReveal(revealConfig);


	/* =========================
	   Detect Mobile Device
	============================*/
	var isMobile = {
	    Android: function() {
	        return navigator.userAgent.match(/Android/i);
	    },
	    BlackBerry: function() {
	        return navigator.userAgent.match(/BlackBerry/i);
	    },
	    iOS: function() {
	        return navigator.userAgent.match(/iPhone|iPad|iPod/i);
	    },
	    Opera: function() {
	        return navigator.userAgent.match(/Opera Mini/i);
	    },
	    Windows: function() {
	        return navigator.userAgent.match(/IEMobile/i);
	    },
	    any: function() {
	        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
	    }
	};


	/* ===========================
	   jQuery One Page Navigation
	==============================*/
	$('#main-nav').onePageNav({
	    filter: ':not(.external)'
	});


	/* ===========================
	   Custom Smooth Scroll For an Anchor
	==============================*/
	$(function() {
	  $('a.scroll-to[href*=#]:not([href=#])').click(function() {
	    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
	      var target = $(this.hash);
	      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
	      if (target.length) {
	        $('html,body').animate({
	          scrollTop: target.offset().top - 50
	        }, 1000);
	        return false;
	      }
	    }
	  });
	});


	/* ===========================
	   Headhesive JS
	   (sticky header on scroll)
	==============================*/

	// Set headhesive options
    var options = {
        classes: {
            clone:   'header-clone',
            stick:   'header-stick',
            unstick: 'header-unstick'
        }
    };
	var headhesive = new Headhesive('.the-header', options);

	// Remove class of the clone header
	// so we can distinguish between the original and the clone header.
	$('.header-clone').removeClass('the-origin-header');


	/* ==========================
	   Progress Bar Animation
	=============================*/
	var skillbar = $('#skillbar').waypoint({
		handler: function() {
			$('.progress-bar').each(function(){
				$(this).animate({
					width:$(this).attr('data-percent')
				},500)
			})
		},
		offset: '150%'
	});


	/* =================================
	   Swipebox JS
	   (Lightbox for Video & Portfolio)
	====================================*/

	// Swipebox Video
	$( '.swipebox-video' ).swipebox();

	// Swipebox Gallery
	$( '.swipebox' ).swipebox();


	/* =================================
	   CounterUp JS
	====================================*/
    $('.counter').counterUp({
	    delay: 10,
	    time: 1000
	});

	/* =================================
	   AjaxChimp JS
	   (Integrate subscribe form w/ Mailchimp)
	====================================*/
	$('.the-subscribe-form').ajaxChimp({
		callback: mailchimpCallback,
	    url: 'http://worksofwisnu.us6.list-manage.com/subscribe/post?u=b57b4e6ae38c92ac22d92a234&amp;id=17754c49aa'
	    // Replace the URL above with your mailchimp URL (put your URL inside '').
	});

	// callback function when the form submitted, show the notification box
	function mailchimpCallback(resp) {
        if (resp.result === 'success') {
            $('#subscribe-success-notification').addClass('show-up');
        }
        else if (resp.result === 'error') {
             $('#subscribe-error-notification').addClass('show-up');
        }
    }


	/* =================================
	   Add Custom Class to Open Toggle Panel
	====================================*/
	$('.panel-heading a').click(function() {

		var clickElement = $(this);

		if (clickElement.parents('.panel-heading').is('.panel-active')) {
			$('.panel-heading').removeClass('panel-active');
		} else {
			$('.panel-heading').removeClass('panel-active');
			clickElement.parents('.panel-heading').addClass('panel-active');
		}
	});


	/* ==================================
	   Quicksand JS
	   (Filter team photo and portfolio)
	=====================================*/

	// Filter team photo
	var $teamClone = $("#team_grid").clone();

	$(".filter a").click(function(e){
		$(".filter li").removeClass("current");

		var $filterClass = $(this).parent().attr("class");

		if ($filterClass == "all") {
			var $filteredTeam = $teamClone.find("li");
		} else {
			var $filteredTeam = $teamClone.find("li[data-type~="+$filterClass+"]");
		}

		$("#team_grid").quicksand( $filteredTeam, {
			easing: "easeOutSine",
			adjustHeight: "dynamic",
			duration: 500,
			useScaling: true
		});

		$(this).parent().addClass("current");

		e.preventDefault();
	})

	// Filter Portfolio Gallery
	var $portfolioClone = $("#portfolio_grid").clone();

	$(".portfolio-filter a").click(function(e){
		$(".portfolio-filter li").removeClass("current");

		var $filterClass = $(this).parent().attr("class");

		if ($filterClass == "all") {
			var $filteredPortfolio = $portfolioClone.find("li");
		} else {
			var $filteredPortfolio = $portfolioClone.find("li[data-type~="+$filterClass+"]");
		}

		$("#portfolio_grid").quicksand( $filteredPortfolio, {
			easing: "easeOutSine",
			adjustHeight: "dynamic",
			duration: 500,
			useScaling: true
		});

		$(this).parent().addClass("current");

		e.preventDefault();
	})

	// Mobile Select Filter
	$("#mobile-team-filter").click(function(){
		$(this).toggleClass("select-active");
		$("ul.filter").toggleClass("filter-active");
	});

	$("#mobile-portfolio-filter").click(function(){
		$(this).toggleClass("select-active");
		$("ul.portfolio-filter").toggleClass("filter-active");
	});


	/* ==================================
	   Contact Overlay
	   (works with multiple buttons)
	=====================================*/
	var triggerBttn = document.querySelectorAll( '.contact-trigger' );

	var	overlay = document.querySelector( 'div.contact-overlay' ),
		closeBttn = overlay.querySelector( 'a.overlay-close' );
		transEndEventNames = {
			'WebkitTransition': 'webkitTransitionEnd',
			'MozTransition': 'transitionend',
			'OTransition': 'oTransitionEnd',
			'msTransition': 'MSTransitionEnd',
			'transition': 'transitionend'
		},
		transEndEventName = transEndEventNames[ Modernizr.prefixed( 'transition' ) ],
		support = { transitions : Modernizr.csstransitions };

	function toggleOverlay() {
		if( classie.has( overlay, 'open' ) ) {
			classie.remove( overlay, 'open' );
			classie.add( overlay, 'close' );
			$('body').removeClass('overlay-on');
			var onEndTransitionFn = function( ev ) {
				if( support.transitions ) {
					if( ev.propertyName !== 'visibility' ) return;
					this.removeEventListener( transEndEventName, onEndTransitionFn );
				}
				classie.remove( overlay, 'close' );
			};
			if( support.transitions ) {
				overlay.addEventListener( transEndEventName, onEndTransitionFn );
			}
			else {
				onEndTransitionFn();
			}
		}
		else if( !classie.has( overlay, 'close' ) ) {
			$("body").addClass('overlay-on');
			classie.add( overlay, 'open' );
		}
		classie.remove(overlay, 'close');
	}

	var i;
	for (i = 0; i < triggerBttn.length; i++) {
		triggerBttn[i].addEventListener( 'click', toggleOverlay );
	}
	closeBttn.addEventListener( 'click', toggleOverlay );


function formatCurrency(total) {
    var neg = false;
    if(total < 0) {
        neg = true;
        total = Math.abs(total);
    }
    return (neg ? "-R$ " : 'R$ ') + parseFloat(total, 10).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, "R$ 1,").toString();
}

	/* ==================================
	   Contact Form Validation
	=====================================*/
    $('#submit').click(function(e){

        // Stop form submission & check the validation
        e.preventDefault();

        if( $("#submit").hasClass("escondido") ){
            $("#validar").click();
            return;
        }

        // Variable declaration
        var error = false;
        var quantidade = $('#quantidade').val();
        var cupom = $('#cupom').val();
        var vlrunit = $('#vlrunit').val();
        var vlrtotal = $('#vlrtotal').val();
        var nome = $('#nome').val();
        var telefone = $('#telefone').val();
        var data_nascimento = $('#data_nascimento').val();
        var email = $('#email').val();
        var cpf = $('#cpf').val();
        var cep = $('#cep').val();
        var nro = $('#nro').val();

        var nrocartao = $('#nrocartao').val();
        var nome_cartao = $('#nome_cartao').val();
        var data_expiracao = $('#data_expiracao').val();
        var cod_seguranca = $('#cod_seguranca').val();
        // var message = $('#message').val();

    	// Form field validation
        if(quantidade.lenght == 0){
            $('#quantidade').val("1");
        }
        if(cupom.length == 0){
            var error = true;
            $('#cupom').parent('div').addClass('field-error');
        }else{
            $('#cupom').parent('div').removeClass('field-error');
        }
        if(vlrunit.length == 0){
            var error = true;
            $('#vlrunit').parent('div').addClass('field-error');
        }else{
            $('#vlrunit').parent('div').removeClass('field-error');
        }
        if(vlrtotal.length == 0){
            var error = true;
            $('#vlrtotal').parent('div').addClass('field-error');
        }else{
            $('#vlrtotal').parent('div').removeClass('field-error');
        }
        if(nome.length == 0){
            var error = true;
            $('#nome').parent('div').addClass('field-error');
        }else{
            $('#nome').parent('div').removeClass('field-error');
        }
        if(telefone.length == 0){
            var error = true;
            $('#telefone').parent('div').addClass('field-error');
        }else{
            $('#telefone').parent('div').removeClass('field-error');
        }
        if(email.length == 0 || email.indexOf('@') == '-1'){
            var error = true;
            $('#email').parent('div').addClass('field-error');
        }else{
            $('#email').parent('div').removeClass('field-error');
        }
        if(data_nascimento.length == 0){
            var error = true;
            $('#data_nascimento').parent('div').addClass('field-error');
        }else{
            $('#data_nascimento').parent('div').removeClass('field-error');
        }
        if(cpf.length == 0 || !valida_cpf(cpf) ){
            var error = true;
            $('#cpf').parent('div').addClass('field-error');
        }else{
            $('#cpf').parent('div').removeClass('field-error');
        }
        if(cep.length == 0){
            var error = true;
            $('#cep').parent('div').addClass('field-error');
        }else{
            $('#cep').parent('div').removeClass('field-error');
        }
        if(nro.length == 0){
            var error = true;
            $('#nro').parent('div').addClass('field-error');
        }else{
            $('#nro').parent('div').removeClass('field-error');
        }

        if( $.md5( cupom.toLowerCase() ) != CP_FRE ){
            //CARTAO DE CREDITO
            if(nrocartao.length == 0){
                var error = true;
                $('#nrocartao').parent('div').addClass('field-error');
            }else{
                $('#nrocartao').parent('div').removeClass('field-error');
            }
            if( !moip.creditCard.isValid(nrocartao) ){
                var error = true;
                $('#nrocartao').parent('div').addClass('field-error');
            }else{
                $('#nrocartao').parent('div').removeClass('field-error');
            }
            if(nome_cartao.length == 0){
                var error = true;
                $('#nome_cartao').parent('div').addClass('field-error');
            }else{
                $('#nome_cartao').parent('div').removeClass('field-error');
            }
            if(data_expiracao.length == 0){
                var error = true;
                $('#data_expiracao').parent('div').addClass('field-error');
            }else{
                $('#data_expiracao').parent('div').removeClass('field-error');
            }

            if( !moip.creditCard.isExpiryDateValid(data_expiracao.split("/")[0], data_expiracao.split("/")[1]) ){
                var error = true;
                $('#data_expiracao').parent('div').addClass('field-error');
            }else{
                $('#data_expiracao').parent('div').removeClass('field-error');
            }
            if(cod_seguranca.length == 0){
                var error = true;
                $('#cod_seguranca').parent('div').addClass('field-error');
            }else{
                $('#cod_seguranca').parent('div').removeClass('field-error');
            }
            if( !moip.creditCard.isSecurityCodeValid(nrocartao, cod_seguranca) ){
                var error = true;
                $('#cod_seguranca').parent('div').addClass('field-error');
            }else{
                $('#cod_seguranca').parent('div').removeClass('field-error');
            }
        }
        // if(message.length == 0){
        //     var error = true;
        //     $('#message').parent('div').addClass('field-error');
        // }else{
        //     $('#message').parent('div').removeClass('field-error');
        // }

        if(error == true){
            mostrarMensagem("Falta preencher campos obrigatórios, por favor verifique o(s) campo(s) marcados em vermelho.");
        }

        if(error == false){
            waitingDialog.show('Aguarde enquanto validamos o pagamento e geramos seus Super Savers Eletrônico');
            // toggleOverlay();

            // Get some values from elements on the page:
            var $form = $("#contact-form"),
                url = $form.attr( "action" );

            //Get all data from inputs
            var formData = $form.serializeFormJSON()

            // Send the data using post
            var posting = $.post( url, formData );

            // // Put the results in a div
            posting.done(function( data ) {
                if(data.sucesso == 'Sucesso'){
                    if(data.tudogratis == false){
                        $("#infopagto").removeClass("escondido");
                        waitingDialog.message('Apenas mais um instante...');
                        //Show confirm dialog
                        // $("#ctoken").html(data.token);
                        $("#MoipWidget").attr("data-token", data.token);

                        // $("#confirmbutton").click(pagarMoip);
                        window.venda = data.venda
                        window.id_proprio_venda = data.id_proprio
                        pagarMoip(data.dados_retorno);  // Return methods are: moipSuccess and moipError above
                    }else{
                        $("#infopagto").addClass("escondido");
                        //Inseriu o cupom gratuito
                        window.venda = data.venda
                        moipSuccess({"Status":"freetotal"});
                    }
                }else if (data.sucesso == "Acabou"){
                    waitingDialog.hide();
                    mostrarMensagem('Infelizmente nossos estoques se esgotaram! Aguarde nova remessa.', true);
                }else{
                    waitingDialog.hide();
                    // toggleOverlay();
                    //Neste caso em data.token vem a mensagem de erro
                    mostrarMensagem('Ocorreu uma falha no pagamento: '+data.token, true);
                }
            });
        }
    });

    var limpaFormGeral = function(top){
        if(top){
            $("#contact-form").
                find("input[type=text], input[type=email],  input[type=number], textarea").
                not("#quantidade, #cupom").
                val("");
        }else{
            $("#contact-form").find("input[type=text], input[type=email],  input[type=number], textarea").val("");
        }
        $(".valores").addClass("escondido");
    }

    $('#confirmpagto').modal({
        'keyboard': false,
        'backdrop': 'static',
        'show': false
    });

    $('#aguardapagto').modal({
        'keyboard': false,
        'backdrop': 'static',
        'show': false
    });


    moipSuccess = function(data){
        if(data.Status == "Cancelado"){
            // Erro na transacao
            waitingDialog.hide();

            mostrarMensagem("Cartão negado: Dados inválidos, verifique as informações", true);

            // if(data.Classificacao.Descricao != null && data.Classificacao.Descricao != ""){
            //     mostrarMensagem("Seu pagamento não foi processado: " + data.Classificacao.Descricao, true);
            // }else{
            //     mostrarMensagem("Seu pagamento não foi processado pela instituição.", true);
            // }

            return;
        }else if(data.Status == "Autorizado" || data.Status == "freetotal"){
            waitingDialog.message('Gerando seus códigos...');
            $('#sse li').remove();
            var posting = $.post( "/ss", {"q":$("#quantidade").val(),"t":window.venda} );
            // var posting = $.post( "/ss", {"q":$("#quantidade").val(),"t":$("#MoipWidget").attr("data-token")} );
            posting.done(function( data ) {
                for( var codigo in data.codigos){
                    $("#sse").append(
                        $("<li>").text(data.codigos[codigo]))
                }
                waitingDialog.hide();
                $('#confirmpagto').modal('show');
                // alert('Sucesso no pagto\n' + JSON.stringify(data));
                // window.open(data.url);
                limpaFormGeral();
                reiniciarform();
                toggleOverlay();
            });
        }else{
            waitingDialog.hide();
            $("#nropedido").html(window.id_proprio_venda);
            $('#aguardapagto').modal('show');
        }
    }
    moipError = function(data){
        waitingDialog.hide();
        // toggleOverlay();
        if(Array.isArray(data)){
            mostrarMensagem('Falha no pagto: ' + data[0].Mensagem);
        }else{
            mostrarMensagem('Falha no pagto: ' + data.Mensagem);
        }
        // alert('Falha no pagto\n' + JSON.stringify(data));
    }
    var pagarMoip = function(settings){ //*AQUI VOCÊ DEVE COLOCAR O NOME DA FUNCAO A SER CAHAMADO
      MoipWidget(settings);//*AQUI VOCÊ DEVE SETAR O JSON PARA QUE O MOIP PROCESSE
    }

    $('#tofeaturettes').click(function(){
        $('html, body').animate({
            scrollTop: $( $.attr(this, 'href') ).offset().top
        }, 500);
        return false;
    });

    var showCardType = function(){
        $(".card-picture").addClass("escondido");
        var card = moip.creditCard.cardType($(this).val());
        $("#cardtype").val(card);
        if(card != null && card != undefined){
            $("#c"+card.brand.toLowerCase()).removeClass("escondido");
        }else{
            $("#ccartao").removeClass("escondido");
        }
    };
    $("#nrocartao").change(showCardType);
    $("#nrocartao").change();

    var mostrarMensagem = function(mensagem, manterAberto){
        $("#subscribe-error-notification .mensagem").html(mensagem);
        $("#subscribe-error-notification").addClass('show-up');
        if(!manterAberto){
            setTimeout(function () {
                $("#subscribe-error-notification").removeClass('show-up');
            }, 4000);
        }
    }

    var colocaValor = function(){
        var cupom = $("#cupom").val();
        var qtd = $("#quantidade").val();
        if( CP_DES.indexOf( $.md5(cupom.toLowerCase()) ) > -1 ){
            $("#vlrunit").val( formatCurrency(VL_ING)+" (até "+VL_DES+"% de desconto)")
            $("#vlrtotal").val( formatCurrency(qtd * VL_ING) )
        }else{
            if( CP_FRE.indexOf($.md5(cupom.toLowerCase())) > -1 ){
                $("#vlrunit").val("R$ 0,00 (100% de desconto)")
                $("#vlrtotal").val("R$ 0,00")
            }
        }
    }
    var priceValue = function(event){

        // event.preventDefault();

        validaQuantidade();
        validaCupom();

        var qtd = $("#quantidade").val();

        var cupom = $("#cupom").val();
        if( qtd != null && qtd > 0 && qtd <= 10 && cupom.length > 0 ){
            if( $.md5( cupom.toLowerCase() ) == CP_DES ){
                $(".valores").removeClass("escondido");
                $(".dadospessoais").removeClass("escondido");
                $(".infocartao").removeClass("escondido");
                $("#vlrunit").val( formatCurrency(VL_ING)+" (até "+VL_DES+"% de desconto)")
                $("#vlrtotal").val( formatCurrency(qtd * VL_ING) )
                $("#nome").focus();

                $("#submit").removeClass("escondido");
            }else{
                if( $.md5( cupom.toLowerCase() ) == CP_FRE ){
                    $(".valores").removeClass("escondido");
                    $(".dadospessoais").removeClass("escondido");
                    $(".infocartao").addClass("escondido");
                    $("#vlrunit").val("R$ 0,00 (100% de desconto)")
                    $("#vlrtotal").val("R$ 0,00")
                    $("#nome").focus();

                    $("#submit").removeClass("escondido");

                }else{
                    $(".dadospessoais").addClass("escondido");
                    $(".valores").addClass("escondido");
                    $(".infocartao").addClass("escondido");

                    $("#cupom").focus();
                }
            }
        }else{
            $(".valores").addClass("escondido");
        }
    };

    var reiniciarform = function(){
        $(".dadospessoais").addClass("escondido");
        $(".valores").addClass("escondido");
        $(".infocartao").addClass("escondido");
        $("#submit").addClass("escondido");
        // limpaFormGeral(true);
    }
    var validaQuantidade = function(event){
        var qtd = $("#quantidade").val();
        if(qtd<1 || qtd>10){
            $('#quantidade').parent('div').addClass('field-error');
            mostrarMensagem("Quantidade inválida. Deve ser entre 1 e 10");
            $("#quantidade").focus()
            return;
        }else{
            $('#quantidade').parent('div').removeClass('field-error');
            colocaValor();
        }
    }
    var validaCupom = function(){
        var cupom = $("#cupom").val();
        if( $.md5( cupom.toLowerCase() ) != CP_DES &&
            $.md5( cupom.toLowerCase() ) != CP_FRE ){
            $('#cupom').parent('div').addClass('field-error');
            mostrarMensagem("Cupom inválido!");
            $("#cupom").focus()
            return;
        }else{
            $('#cupom').parent('div').removeClass('field-error');
        }
    }
    var validaCampoObrigatorio = function(){
        var valor = $(this).val();
        if(valor.length == 0){
            $(this).parent('div').addClass('field-error');
        }else{
            $(this).parent('div').removeClass('field-error');
        }
    }
    var validaCampoEmail = function(){
        var valor = $(this).val();
        if(valor.length == 0 || valor.indexOf('@') == '-1'){
            $(this).parent('div').addClass('field-error');
            mostrarMensagem("Email inválido");
        }else{
            $(this).parent('div').removeClass('field-error');
        }
    }
    var validaCpfObrigatorio = function(){
        var valor = $(this).val();
        if(valor.length == 0 ){
            $(this).parent('div').addClass('field-error');
            mostrarMensagem("CPF não informado");
        }else if( !valida_cpf(valor) ){
            $(this).parent('div').addClass('field-error');
            mostrarMensagem("CPF Inválido");
        }else{
            $(this).parent('div').removeClass('field-error');
        }
    }
    var validaCartaoObrigatorio = function(){
        var valor = $(this).val();
        if(valor.length == 0 || !moip.creditCard.isValid(valor) ){
            $(this).parent('div').addClass('field-error');
            mostrarMensagem("Cartão negado");
        }else{
            $(this).parent('div').removeClass('field-error');
        }
    }
    var validaDataCartaoObrigatorio = function(){
        var valor = $(this).val();
        if(valor.length == 0 || !moip.creditCard.isExpiryDateValid(valor.split("/")[0], valor.split("/")[1] ) ){
            $(this).parent('div').addClass('field-error');
            mostrarMensagem("Data de expiração inválida");
        }else{
            $(this).parent('div').removeClass('field-error');
        }
    }
    var validaCodSegCartaoObrigatorio = function(){
        var valor = $(this).val();
        if(valor.length == 0 || !moip.creditCard.isSecurityCodeValid($("#nrocartao").val(), valor) ){
            $(this).parent('div').addClass('field-error');
            mostrarMensagem("Código de segurança inválido");
        }else{
            $(this).parent('div').removeClass('field-error');
        }
    }
    $("#nome").blur(validaCampoObrigatorio);
    $("#telefone").blur(validaCampoObrigatorio);
    $("#email").blur(validaCampoEmail);
    $("#data_nascimento").blur(validaCampoObrigatorio);
    $("#cpf").blur(validaCpfObrigatorio);
    $("#nro").blur(validaCampoObrigatorio);
    $("#nrocartao").blur(validaCartaoObrigatorio);
    $("#nome_cartao").blur(validaCampoObrigatorio);
    $("#data_expiracao").blur(validaDataCartaoObrigatorio);
    $("#cod_seguranca").blur(validaCodSegCartaoObrigatorio);

    $("#cupom").change(reiniciarform);
    $("#cupom").blur(validaCupom);
    // $("#quantidade").change(reiniciarform);
    $("#quantidade").blur(validaQuantidade);
    $("#validar").click(priceValue);

    var maskOpt = {selectOnFocus: true};
    $('#quantidade').mask('00',maskOpt);
    $('#cep').mask('00000-000',maskOpt);
    $('#nro').mask('#######0',maskOpt);
    $('#cpf').mask('000.000.000-00',maskOpt);
    $('#nrocartao').mask('0000-0000-0000-0000',maskOpt);
    $('#data_nascimento').mask('00/00/0000',maskOpt);
    $('#data_expiracao').mask('00/0000',maskOpt);
    $('#cod_seguranca').mask('000',maskOpt);
    var SPMaskBehavior = function (val) {
      return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
    spOptions = {
      onKeyPress: function(val, e, field, options) {
          field.mask(SPMaskBehavior.apply({}, arguments), options);
        },
      selectOnFocus: true
    };
    $('#telefone').mask(SPMaskBehavior, spOptions);

    var limpa_formulário_cep = function(){
        $("#rua").val("");
        $("#nro").val("");
        $("#complemento").val("");
        $("#bairro").val("");
        $("#cidade").val("");
        $("#uf").val("");
    };

    $("#cep").blur(function(){
                //Nova variável "cep" somente com dígitos.
                var cep = $(this).val().replace(/\D/g, '');

                //Verifica se campo cep possui valor informado.
                if (cep != "") {

                    //Expressão regular para validar o CEP.
                    var validacep = /^[0-9]{8}$/;

                    //Valida o formato do CEP.
                    if(validacep.test(cep)) {

                        //Preenche os campos com "..." enquanto consulta webservice.
                        $("#rua").val("...")
                        $("#bairro").val("...")
                        $("#cidade").val("...")
                        $("#uf").val("...")

                        //Consulta o webservice viacep.com.br/
                        $.getJSON("//viacep.com.br/ws/"+ cep +"/json/?callback=?", function(dados) {

                            if (!("erro" in dados)) {
                                //Atualiza os campos com os valores da consulta.
                                $("#rua").val(dados.logradouro);
                                $("#bairro").val(dados.bairro);
                                $("#cidade").val(dados.localidade);
                                $("#uf").val(dados.uf);
                                $("#nro").focus();
                                $('#cep').parent('div').removeClass('field-error');
                            } //end if.
                            else {
                                //CEP pesquisado não foi encontrado.
                                limpa_formulário_cep();
                                $('#cep').parent('div').addClass('field-error');
                                mostrarMensagem("Seu cep não foi encontrado. Corrija e tente novamente.");
                            }
                        });
                    } //end if.
                    else {
                        //cep é inválido.
                        limpa_formulário_cep();
                        $('#cep').parent('div').addClass('field-error');
                        mostrarMensagem("Seu cep está inválido. Corrija e tente novamente.");
                    }
                } //end if.
                else {
                    //cep sem valor, limpa formulário.
                    limpa_formulário_cep();
                    $('#cep').parent('div').addClass('field-error');
                    mostrarMensagem("Seu cep não foi informado.");
                }
    })


    /* ==================================
	   Hero Form Validation
	// =====================================*/
	// $('#hero-submit').click(function(e){

 //        // Stop form submission & check the validation
 //        e.preventDefault();

 //        // Variable declaration
 //        var error = false;
 //        var fname = $('#hero-fname').val();
 //        var email = $('#hero-email').val();
 //        var username = $('#hero-username').val();

 //     	// Form field validation
 //        if(fname.length == 0){
 //            var error = true;
 //            $('#hero-fname').parent('div').addClass('field-error');
 //        }else{
 //            $('#hero-fname').parent('div').removeClass('field-error');
 //        }
 //        if(email.length == 0 || email.indexOf('@') == '-1'){
 //            var error = true;
 //            $('#hero-email').parent('div').addClass('field-error');
 //        }else{
 //            $('#hero-email').parent('div').removeClass('field-error');
 //        }
 //        if(username.length == 0){
 //            var error = true;
 //            $('#hero-username').parent('div').addClass('field-error');
 //        }else{
 //            $('#hero-username').parent('div').removeClass('field-error');
 //        }

 //        if(error == true){
 //        	$('#hero-error-notification').addClass('show-up');
 //        }else{
 //           $('#hero-error-notification').removeClass('show-up');
 //        }

 //        if(error == false){
 //            $.post("hero-form.php", $("#register-form").serialize(),function(result){
 //                if(result == 'sent'){
 //                    $('#hero-success-notification').addClass('show-up');
 //                    $('#hero-submit').addClass('disabled');
 //                }
 //            });
 //        }
 //    });


	// Function to close the Notification
    $('a.notification-close').click(function(){
	    $("#subscribe-error-notification").removeClass('show-up');
        // $(this).parent('div').fadeOut(200);
    });


	/* ==========================
	   Custom Popover
	   (for Language Selection)
	=============================*/
    $("[data-toggle=popover]").popover();


	/* ==============================
	   Change Footer Background
	   (when Social Icons hovered)
	=================================*/
	if(!isMobile.any()){
		$(".footer-social .icon-facebook-with-circle").hover(function(){$("#main-footer").toggleClass("footer-facebook-hovered")});
		$(".footer-social .icon-twitter-with-circle").hover(function(){$("#main-footer").toggleClass("footer-twitter-hovered")});
		$(".footer-social .icon-linkedin-with-circle").hover(function(){$("#main-footer").toggleClass("footer-linkedin-hovered")});
		$(".footer-social .icon-instagram-with-circle").hover(function(){$("#main-footer").toggleClass("footer-instagram-hovered")});
		$(".footer-social .icon-google-with-circle").hover(function(){$("#main-footer").toggleClass("footer-google-hovered")});
		$(".footer-social .icon-dribbble-with-circle").hover(function(){$("#main-footer").toggleClass("footer-dribbble-hovered")});
		$(".footer-social .icon-pinterest-with-circle").hover(function(){$("#main-footer").toggleClass("footer-pinterest-hovered")});
		$(".footer-social .icon-vimeo-with-circle").hover(function(){$("#main-footer").toggleClass("footer-vimeo-hovered")});
	}

});

(function ($) {
    $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
})(jQuery);


$('.selectpicker').selectpicker({"width":"auto"});

$("#verfilmes").click(function(){
    var url = $("#cinemas").val();
    window.open(url);
});
