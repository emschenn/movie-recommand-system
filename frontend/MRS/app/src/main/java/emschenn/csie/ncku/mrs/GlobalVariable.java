package emschenn.csie.ncku.mrs;
import android.app.Application;

public class GlobalVariable extends Application {
    private String URL = "http://192.168.210.22:8000/post/";
    //修改 變數値
    public void setURL(String url){
        this.URL = url;
    }
    public String getURL() {
        return URL;
    }
}