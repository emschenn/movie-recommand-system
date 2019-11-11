package emschenn.csie.ncku.mrs;

import android.content.Context;
import android.content.Intent;
import android.webkit.JavascriptInterface;


public class AndroidtoJs extends Object {
    Context mContext;

    /** Instantiate the interface and set the context */
    AndroidtoJs(Context c) {
        mContext = c;
    }

    // 定义JS需要调用的方法
    // 被JS调用的方法必须加入@JavascriptInterface注解
    @JavascriptInterface
    public void restart() {
        System.out.println("JS调用了Android的hello方法");
        Intent intent = new Intent(mContext, MainActivity.class);
        mContext.startActivity(intent);
        //c.finish;
    }
}