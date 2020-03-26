
import java.util.List;
import java.util.ArrayList;

public class Desencriptar {

    List<Integer> palabraAAscii;
    String bitsDeAscii;
    List<String> numBytes;
    List<Integer> asciis;
    String palabraDesencriptada;

    char[] tabla = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '='};

    public Desencriptar(String palabra) {
        List<Integer> palabraAAscii = wordToAscii(palabra);
        this.palabraAAscii = palabraAAscii;
        
        String bitsDeAscii = getAsciiBits(palabraAAscii, 6);
        this.bitsDeAscii = bitsDeAscii;
        
        List<String> numBytes = groupBitsInCompleteBytes(bitsDeAscii);
        this.numBytes = numBytes;
        
        List<Integer> asciis = getAsciis(numBytes);
        this.asciis = asciis;
        
        String palabraDesencriptada = changeToWordAgainWithAscii(asciis);
        this.palabraDesencriptada = palabraDesencriptada;
    }
    
    List<Integer> getPalabraAAscii(){
        return palabraAAscii;
    }
    
    String getBitsDeAscii(){
        return bitsDeAscii;
    }
    
    List<String> getNumBytes(){
        return numBytes;
    }
    
    List<Integer> getAsciis(){
        return asciis;
    }
    
    String getPalabraDesencriptada(){
        return palabraDesencriptada;
    }
    
    String changeToWordAgainWithAscii(List<Integer> asciis){
        String word = "";
        for(int i : asciis){
            word += (char)i;
        }
        
        return word;
    }

    List<Integer> getAsciis(List<String> bytesArr) {
        List<Integer> asciis = new ArrayList<>();

        for (int i = 0; i < bytesArr.size(); i++) {
            asciis.add(0);
            int potencia = 0;
            int numComodin = 0;
            for (int j = 7; j > -1; j--) {
                if (bytesArr.get(i).charAt(j) == '1') {
                    numComodin += (int) Math.pow(2, potencia);
                    potencia++;
                    continue;
                }
                potencia++;
            }
            asciis.set(i, numComodin);
        }
        
        return asciis;
    }

    List<String> groupBitsInCompleteBytes(String bits) {
        int numBytes = bits.length() / 8;
        List<String> bytesArr = new ArrayList<>();

        for (int i = 0; i < numBytes; i++) {
            bytesArr.add("");
            String palabraComodin = "";
            for (int j = 0; j < 8; j++) {
                palabraComodin += bits.charAt(i * 8 + j);
            }
            bytesArr.set(i, palabraComodin);
        }

        return bytesArr;
    }

    String toBits(int numero, int howManyBits) {
        String bits = "";
        int potencia = howManyBits - 1;
        while (potencia > -1) {
            if (numero - Math.pow(2, potencia) < 0) {
                bits += "0";
                potencia--;
            } else {
                bits += "1";
                numero -= Math.pow(2, potencia);
                potencia--;
            }
        }
        return bits;
    }

    public String getAsciiBits(List<Integer> asciis, int howManyBits) {
        String bits = "";
        for (int i : asciis) {
            bits += toBits(i, howManyBits);
        }
        return bits;
    }

    List<Integer> wordToAscii(String word) {
        List<Integer> asciis = new ArrayList<>();
        for (char i : word.toCharArray()) {
            if (i == '=') {
                continue;
            } else if ((int) i - 65 >= 0 && (int) i - 65 <= 25) { //Mayusculas
                asciis.add((int) i - 65);
            } else if ((int) i - 97 + 26 >= 26 && (int) i - 97 + 26 <= 51) { //Minusculas
                asciis.add((int) i - 97 + 26);
            } else if ((int) i - 48 + 52 >= 52 && (int) i - 48 + 52 <= 61) { //Numeros
                asciis.add((int) i - 48 + 52);
            } else if (i == '+') {
                asciis.add(62);
            } else if (i == '/') {
                asciis.add(63);
            }
        }
        
        return asciis;
    }

}
