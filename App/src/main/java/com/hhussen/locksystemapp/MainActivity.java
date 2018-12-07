package com.hhussen.locksystemapp;

import android.os.Handler;
import android.os.HandlerThread;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;

public class MainActivity extends AppCompatActivity {
    //Declare required variables
    private Button bUnlockDoor;
    private Button bLockDoor;

    private TextView tDoorStatus; //Unimplemented

    private String UNLOCK_MESSAGE = "3";
    private String LOCK_MESSAGE = "4";

    private HandlerThread readThread; //Unimplemented
    private Handler mHandler; //Unimplemented

    DatagramSocket dsocket;
    DatagramPacket packet;
    byte[] buffer;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        //handler.postDelayed(udpClient, 1000);

        bUnlockDoor = (Button) findViewById(R.id.unlockButton);
        bLockDoor = (Button) findViewById(R.id.lockButton);

        bUnlockDoor.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                updateDoorState(UNLOCK_MESSAGE);
            }
        });

        bLockDoor.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                updateDoorState(LOCK_MESSAGE);
            }
        });

    }

    public void updateDoorState(String message) {
        try {
            String target_address = "192.168.43.206";
            int port = 8888;

            byte[] sending = message.getBytes();

            // Get the internet address of the specified host
            InetAddress address = InetAddress.getByName(target_address);

            // Initialize a datagram packet with data and address
            DatagramPacket packet = new DatagramPacket(sending, sending.length,
                    address, port);

            // Create a datagram socket to send the packets, then close it
            DatagramSocket dsocket = new DatagramSocket();
            dsocket.send(packet);
            dsocket.close();
        } catch (Exception e) {
            System.err.println(e);
        }
    }

/* Implemented, not working -> Would print the doorState in a textView
    public void getDoorState(String message) {
        try {
            String target_address = "192.168.43.206";
            int port = 8888; //Random Port

            byte[] sending = message.getBytes();

            // Get the internet address of the specified host
            InetAddress address = InetAddress.getByName(target_address);

            // Initialize a datagram packet with data and address
            DatagramPacket packet = new DatagramPacket(sending, sending.length,
                    address, port);

            // Create a datagram socket, send the packet through it, close it.
            DatagramSocket dsocket = new DatagramSocket();
            dsocket.send(packet);
            dsocket.close();
        } catch (Exception e) {
            System.err.println(e);
        }
    }
*/
}