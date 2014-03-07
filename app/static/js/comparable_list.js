$(function(){
    var selectedArr = [];
    var findElem = function(key){
        var index = -1;
        $.each(selectedArr, function(i , val){
            if(val == key){
                index = i;
                return;
            }
        });
        return index;
    };
   $('input.product-checkbox-input').click(function(e){
       //e.preventDefault();
       var display = $('#selectedItemCnt');
       var key = $(this).attr('data-attr');
       var idx;

       if((idx = findElem(key)) != -1){
           var last = selectedArr.length - 1;
           var temp = selectedArr[last];
           selectedArr[last] = selectedArr[idx];
           selectedArr[idx] = temp;
           selectedArr.pop();

       }else{
           selectedArr.push(key);
       }

       display.text(selectedArr.length);
   });
});
