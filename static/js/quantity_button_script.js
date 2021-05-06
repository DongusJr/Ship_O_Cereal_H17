$('.btn-number').click(function(e){
    e.preventDefault();

    let type = $(this).attr('data-type');
    let input = $("input[name='quant']");
    let currentVal = parseInt(input.val());
    if (!isNaN(currentVal)){
        if (type === 'minus') {
            if (currentVal > input.attr('min')) {
                input.val(currentVal - 1).change();
            }
            if(parseInt(input.val()) === input.attr('min')){
                $(this).attr('disabled', true);
            }
        } else if(type === 'plus') {
            if (currentVal < input.attr('max')) {
                input.val(currentVal + 1).change();
            }
            if(parseInt(input.val()) === input.attr('max')){
                $(this).attr('disabled', true);
            }
        }
    } else {
        input.val(0);
    }
});

$('.input-number').focusin(function(){
   $(this).data('oldValue', $(this).val());
});

$('.input-number').change(function() {

    minValue =  parseInt($(this).attr('min'));
    maxValue =  parseInt($(this).attr('max'));
    valueCurrent = parseInt($(this).val());

    name = $(this).attr('name');
    if(valueCurrent >= minValue) {
        $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        $(this).val($(this).data('oldValue'));
    }
    if(valueCurrent <= maxValue) {
        $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
    } else {
        $(this).val($(this).data('oldValue'));
    }
});