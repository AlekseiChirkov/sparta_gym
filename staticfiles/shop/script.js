function myFunc(){
    $(document).ready(function(){
        flag=1;
         $('#next').click(function(){
           if(flag==0)
            {
               $('.slide1').css('z-index', '99');
               $('.slide2').css('z-index', '89');
               $('.slide3').css('z-index', '89');
               $('.slide4').css('z-index', '79');
               $('.slide5').css('z-index', '79');
               $('.slide1').css('transform', 'translateX(0px) scale(1.5)');
               $('.slide2').css('transform', 'translateX(-200px) scale(1.2)');
               $('.slide3').css('transform', 'translateX(200px) scale(1.2)');
               $('.slide4').css('transform', 'translateX(-300px) scale(1)');
               $('.slide5').css('transform', 'translateX(300px) scale(1)');
               flag=1;
            }
            else if(flag==1)
            {
               $('.slide2').css('z-index', '99');
               $('.slide4').css('z-index', '89');
               $('.slide1').css('z-index', '89');
               $('.slide5').css('z-index', '79');
               $('.slide3').css('z-index', '79');
               $('.slide2').css('transform', 'translateX(0px) scale(1.5)');
               $('.slide4').css('transform', 'translateX(-200px) scale(1.2)');
               $('.slide1').css('transform', 'translateX(200px) scale(1.2)');
               $('.slide5').css('transform', 'translateX(-300px) scale(1)');
               $('.slide3').css('transform', 'translateX(300px) scale(1)');
               flag=2;
            }
            else if(flag==2)
            {
               $('.slide4').css('z-index', '99');
               $('.slide5').css('z-index', '89');
               $('.slide2').css('z-index', '89');
               $('.slide3').css('z-index', '79');
               $('.slide1').css('z-index', '79');
               $('.slide4').css('transform', 'translateX(0px) scale(1.5)');
               $('.slide5').css('transform', 'translateX(-200px) scale(1.2)');
               $('.slide2').css('transform', 'translateX(200px) scale(1.2)');
               $('.slide3').css('transform', 'translateX(-300px) scale(1)');
               $('.slide1').css('transform', 'translateX(300px) scale(1)');
               flag=3;
            }
            else if(flag==3)
            {
               $('.slide5').css('z-index', '99');
               $('.slide3').css('z-index', '89');
               $('.slide4').css('z-index', '89');
               $('.slide1').css('z-index', '79');
               $('.slide2').css('z-index', '79');
               $('.slide5').css('transform', 'translateX(0px) scale(1.5)');
               $('.slide3').css('transform', 'translateX(-200px) scale(1.2)');
               $('.slide4').css('transform', 'translateX(200px) scale(1.2)');
               $('.slide1').css('transform', 'translateX(-300px) scale(1)');
               $('.slide2').css('transform', 'translateX(300px) scale(1)');
               flag=4;
            }
            else if(flag==4)
            {
               $('.slide3').css('z-index', '99');
               $('.slide1').css('z-index', '89');
               $('.slide5').css('z-index', '89');
               $('.slide2').css('z-index', '79');
               $('.slide4').css('z-index', '79');
               $('.slide3').css('transform', 'translateX(0px) scale(1.5)');
               $('.slide1').css('transform', 'translateX(-200px) scale(1.2)');
               $('.slide5').css('transform', 'translateX(200px) scale(1.2)');
               $('.slide2').css('transform', 'translateX(-300px) scale(1)');
               $('.slide4').css('transform', 'translateX(300px) scale(1)');
               flag=0;
            }
        });
    });
}
