/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import AVS from 'alexa-voice-service';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  WebView
} from 'react-native';

const avs = new AVS({
  debug: true,
  clientId: 'amzn1.application-oa2-client.eec9ebc38e7d4a9eb06c653bd474cd1b',
  deviceId: 'dobby_alexa_device',
  deviceSerialNumber: 123,
  redirectUri: 'https://776c2c44.ngrok.io/avsauth'
});

export default class voicepay_app extends Component {
  constructor() {
    super()
    this.state  = {'url' : 'http://google.com'}
    avs.getLoginURL()
      .then(url => {
        console.log(url)
        this.setState({'url' : url})
      })
      .catch((data) => {
        console.log(data);
      });

  }
  render() {

    return (
      <View style={styles.container}>

        <WebView
            ref="WEBVIEW_REF"
            styles={styles.webview}
            source={{uri: this.state.url}}
            startInLoadingState={true}
          />

        <Text style={styles.welcome}>
          Welcome to React Native!
        </Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5FCFF',
  },
  webview: {
    flex:1,
    marginTop: 20,
    height: 350,
    width: 350
  },
  welcome: {
    height: 50,
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});

AppRegistry.registerComponent('voicepay_app', () => voicepay_app);
