package com.example.oem.bookapp20;


import android.annotation.SuppressLint;
import android.graphics.Color;
import android.os.AsyncTask;
import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.RatingBar;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;



public class MainActivity extends AppCompatActivity {
    int j = 0;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        final Button button = findViewById(R.id.button);
        final TextView t = findViewById(R.id.textView);
        final TextView desc = findViewById(R.id.description);
        final ImageView image = findViewById(R.id.imageView);
        final Button start = findViewById(R.id.start);
        final ConstraintLayout layout = findViewById(R.id.layout);
        final RatingBar rating = findViewById(R.id.ratingBar);
        @SuppressLint("StaticFieldLeak")
        class MyTask extends AsyncTask<Void, Void, Void> {

            private String title;
            private String imageurl;
            private String text;

            @Override
            protected Void doInBackground(Void... params) {
                Document doc = null;
                String[] sites = new String[]{
                        "https://www.bookclub.ua/catalog/books/pop/product.html?id=47205",
                "https://www.bookclub.ua/catalog/books/adventure/product.html?id=46761",
                "https://www.bookclub.ua/catalog/books/psychology/product.html?id=46807",
                "https://www.bookclub.ua/catalog/books/classic/product.html?id=47207"};
                try {
                            doc = Jsoup.connect(""+sites[j % 4]).get();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                if (doc!=null) {
                    title = doc.title( ).substring(0, doc.title( ).indexOf("Книжн") - 2);
                    text = doc.select("div[class=proddesc]").text();
                    Elements img = doc.select("img.imgprod[src]");
                    imageurl = img.attr("src");

                }else
                    title = "Error";

                return null;
            }

            @Override
            protected void onPostExecute(Void result) {
                super.onPostExecute(result);
                desc.setText(text.substring(0,300));
                t.setText(title);
                Picasso.with(MainActivity.this).
                        load("https://www.bookclub.ua/"+imageurl).
                        into(image);
            }
        }

        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                MyTask m = new MyTask();
                m.execute();
                rating.setRating(0.0f);
                j++;

            }
        });
        start.setOnClickListener(new View.OnClickListener( ) {
            public void onClick(View view) {
                if (!button.isShown()){
                    button.setVisibility(View.VISIBLE);
                    t.setVisibility(View.VISIBLE);
                    desc.setVisibility(View.VISIBLE);
                    image.setVisibility(View.VISIBLE);
                    rating.setVisibility(View.VISIBLE);
                    start.setVisibility(View.INVISIBLE);
                    layout.setBackgroundColor(Color.WHITE);
                }
                MyTask m = new MyTask();
                m.execute();
            }
        });

    }
}
