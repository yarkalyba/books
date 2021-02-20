
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.facebook.AccessToken;
import com.facebook.CallbackManager;
import com.facebook.FacebookCallback;
import com.facebook.FacebookException;
import com.facebook.login.LoginResult;
import com.facebook.login.widget.LoginButton;

import java.util.Arrays;

public class LoginIn extends AppCompatActivity {
    CallbackManager callbackManager = CallbackManager.Factory.create();
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        final String EMAIL = "email";
        final Button continue_b = findViewById(R.id.continue_button);
        continue_b.setOnClickListener(new View.OnClickListener( ) {
            @Override
            public void onClick(View view) {
                Intent go_to_main = new Intent(LoginIn.this,MainActivity.class);
                startActivity(go_to_main);
                finish();
            }
        });
        AccessToken token;
        token = AccessToken.getCurrentAccessToken();

        if (token != null) {
            continue_b.setVisibility(View.VISIBLE);
        }
        final LoginButton loginButton = findViewById(R.id.login_button);
        loginButton.setReadPermissions(Arrays.asList(EMAIL));
        loginButton.registerCallback(callbackManager, new FacebookCallback<LoginResult>() {
            @Override
            public void onSuccess(LoginResult loginResult) {
                continue_b.setVisibility(View.VISIBLE);
            }

            @Override
            public void onCancel() {

            }

            @Override
            public void onError(FacebookException exception) {

            }
        });
    }
        protected void onActivityResult(int requestCode, int resultCode, Intent data)
        {
            super.onActivityResult(requestCode, resultCode, data);
            callbackManager.onActivityResult(requestCode, resultCode, data);
        }

}
