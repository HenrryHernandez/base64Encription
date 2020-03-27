
import java.util.List;
import java.util.ArrayList;


//PUEDE USAR ESTA CLASE QUE INCLUTE EL METODO MAIN PARA PODER HACER PRUEBAS DEL PROGRAMA

public class pruebas {
    public static void main(String args[]) {
        Encriptar en = new Encriptar("qegffqf");
        String palabraEn = en.getPalabraEncriptada();
        System.out.println(palabraEn);
        
        
        Desencriptar desen = new Desencriptar("XcYhn");
        String palabraDesen = desen.getPalabraDesencriptada();
        System.out.println(palabraDesen);
    }
}
