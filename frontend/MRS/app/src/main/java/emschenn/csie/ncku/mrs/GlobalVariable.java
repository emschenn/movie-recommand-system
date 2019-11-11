package emschenn.csie.ncku.mrs;
import android.app.Application;

public class GlobalVariable extends Application {
    private String URL = "http://192.168.43.99:8000";
    //修改 變數値
    public void setURL(String url){
        this.URL = url;
    }
    public String postURL() {
        return URL+"/post/";
    }
    public String addURL() {
        return URL+"/add/";
    }
}