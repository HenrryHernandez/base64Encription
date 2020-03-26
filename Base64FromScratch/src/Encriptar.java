
import java.util.List;
import java.util.ArrayList;

public class Encriptar {

    String palabraBits;
    List<List<String>> bytesDefinidos;
    String palabraEncriptada;

    char[] tabla = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
        'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '='};

    Encriptar(String palabra) {
        String palabraBits = getAsciiBits(getWordAscii(palabra), 8);
        this.palabraBits = palabraBits;

        List<List<String>> bytesDefinidos = difineBytes(palabraBits);
        this.bytesDefinidos = bytesDefinidos;

        String palabraEncriptada = changeToWordAgainWithTable(tabla, bytesDefinidos);
        this.palabraEncriptada = palabraEncriptada;
    }

    String getPalabraBits() {
        return palabraBits;
    }

    List<List<String>> getBytesDefinidos() {
        return bytesDefinidos;
    }

    String getPalabraEncriptada() {
        return palabraEncriptada;
    }

    List<Integer> getBitsAsciis(List<List<String>> bytess) {
        List<Integer> asciis = new ArrayList<>();
        for (int i = 0; i < bytess.size(); i++) {
            for (int j = 0; j < 4; j++) {
                int palabraNumero = 0;
                int potencia = 0;
                asciis.add(0);
                int numeroComodin = 0;
                for (int k = 5; k > -1; k--) {
                    if (bytess.get(i).get(j).charAt(k) == '1') {
                        numeroComodin += (int) Math.pow(2, potencia);
                        potencia++;
                        continue;
                    } else if (bytess.get(i).get(j).charAt(k) == '@') {
                        numeroComodin = (int)(bytess.get(i).get(j).charAt(k));
                        break;
                    }
                    potencia++;
                }
                asciis.set(asciis.size() - 1, numeroComodin);
            }
        }
        return asciis;
    }

    String changeToWordAgainWithTable(char[] tabla, List<List<String>> bytesDefinidos) {
        List<Integer> bytesDefinidos2 = getBitsAsciis(bytesDefinidos);
        String palabraEncriptada = "";
        for (int i : bytesDefinidos2) {
            palabraEncriptada += tabla[i];
        }
        return palabraEncriptada;
    }

    List<List<String>> difineGroupsInBytesOf3(List<List<Character>> bytesArr) {
        List<List<String>> bytesEnTres = new ArrayList<>();
        int seises = bytesArr.get(bytesArr.size() - 1).size() / 6;

        if (seises != 4) {
            if (bytesArr.get(bytesArr.size() - 1).size() - 6 * seises != 0) {
                for (int i = bytesArr.get(bytesArr.size() - 1).size(); i < 6 * (seises + 1); i++) {
                    bytesArr.get(bytesArr.size() - 1).add('0');
                }
            }
            seises = bytesArr.get(bytesArr.size() - 1).size();
        }

        for (int i = seises; i < 24; i++) {
            bytesArr.get(bytesArr.size() - 1).add('@');
        }

        for (int i = 0; i < bytesArr.size(); i++) {
            bytesEnTres.add(new ArrayList<>());
            for (int j = 0; j < 4; j++) {
                bytesEnTres.get(i).add("");
                String palComodin = "";
                for (int k = 0; k < 6; k++) {
                    palComodin += bytesArr.get(i).get(j * 6 + k).toString();
                }
                bytesEnTres.get(i).set(j, palComodin);
            }
        }
        return bytesEnTres;

    }

    public List<List<String>> difineBytes(String bits) {
        int veinticuatros = bits.length() / 24;
        List<List<Character>> bytess = new ArrayList<>();

        for (int i = 0; i < veinticuatros; i++) {
            bytess.add(new ArrayList<>());
            for (int j = 0; j < 24; j++) {
                bytess.get(i).add(bits.charAt(i * 24 + j));
            }
        }

        bytess.add(new ArrayList<>());
        for (int i = veinticuatros * 24; i < bits.length(); i++) {
            bytess.get(veinticuatros).add(bits.charAt(i));
        }

        if (bytess.get(veinticuatros).isEmpty()) {
            bytess.remove(veinticuatros);
        }

        List<List<String>> bytesStrings = new ArrayList<>();
        bytesStrings = difineGroupsInBytesOf3(bytess);
        return bytesStrings;
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

    public List<Integer> getWordAscii(String palabra) {
        List<Integer> list = new ArrayList<>();
        for (char i : palabra.toCharArray()) {
            list.add((int) i);
        }
        return list;
    }

}
