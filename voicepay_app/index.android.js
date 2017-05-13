/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 * @flow
 */

import React, { Component } from 'react';
import AVS from 'alexa-voice-service';
import RNFetchBlob from 'react-native-fetch-blob'
import {
  AppRegistry,
  StyleSheet,
  Text,
  View,
  WebView,
  Switch,
  Slider,
  Button
} from 'react-native';

import {
  Player,
  Recorder,
  MediaStates
} from 'react-native-audio-toolkit';

const avs = new AVS({
  debug: true,
  clientId: 'amzn1.application-oa2-client.eec9ebc38e7d4a9eb06c653bd474cd1b',
  deviceId: 'dobby_alexa_device',
  deviceSerialNumber: 123,
  redirectUri: 'https://776c2c44.ngrok.io/avsauth'
});

let filename = 'test.mp4';

export default class voicepay_app extends Component {
  constructor() {
    super()
    this.state  = {
      url : 'http://google.com',
      playPauseButton: 'Preparing...',
      recordButton: 'Preparing...',

      stopButtonDisabled: true,
      playButtonDisabled: true,
      recordButtonDisabled: true,

      loopButtonStatus: false,
      progress: 0,

      error: null
    }
    avs.getLoginURL()
      .then(url => {
        console.log(url)
        this.setState({'url' : url})
      })
      .catch((data) => {
        console.log(data);
      });
    avs.setToken("Atza|IwEBINy6B67d8KYKhbkFdEUHim090YWBN-BfbkeqbwAuLJAIbRb_QPLT7OMOqzNu7qve4vOYAIlFwlZHyjL7Mcm96CbrwiCDfzbbmra01HFX_M-IKfk66WHWrEr_4rNf7LF0xGYqhOUdoZJpMxzoAk5KfoT6rMB1h2FpsptBjXk-_6wJSLouUTtYuhovsoxy5U0BqdQQwA7MxlEzW8ZEBCiP1snFh1YOx5t4Wxmyn65qNyCDxjjVSO7StHfssHas9oE7thp40cVmbhtGv7ls_ebpRdb0ITo92TV95hi_mByCj5Ek6oBOVHFXvi24G84ZPHXtw3VNgG2T5UN4BOTDWfR3L_AGWRW45TC77pfx1bCcAK9doWgbBbQi4wuxQJOOO8IFCk9vmvqa9Hwvz3V2_SQcvcLFSOIwza2FLw4EP6u50b4aScLXLCK6X4fYtTXQB84h1GXGewojwyxjWi80DGWzQ4RaZ4ADFWdJSJbZBovdHW0L1GGr_P1tjOVVcW7y1MomuGjqSMVaKIdNUAREyWXByRad")

  }
  componentWillMount() {
    this.player = null;
    this.recorder = null;
    this.lastSeek = 0;

    this._reloadPlayer();
    this._reloadRecorder();

    this._progressInterval = setInterval(() => {
      if (this.player && this._shouldUpdateProgressBar()) {// && !this._dragging) {
        this.setState({progress: Math.max(0, this.player.currentTime) / this.player.duration});
      }
    }, 100);
  }

  componentWillUnmount() {
    //console.log('unmount');
    // TODO
    clearInterval(this._progressInterval);
  }

  _shouldUpdateProgressBar() {
  // Debounce progress bar update by 200 ms
    return Date.now() - this.lastSeek > 200;
  }

  _updateState(err) {
    this.setState({
      playPauseButton:      this.player    && this.player.isPlaying     ? 'Pause' : 'Play',
      recordButton:         this.recorder  && this.recorder.isRecording ? 'Stop' : 'Record',

      stopButtonDisabled:   !this.player   || !this.player.canStop,
      playButtonDisabled:   !this.player   || !this.player.canPlay || this.recorder.isRecording,
      recordButtonDisabled: !this.recorder || (this.player         && !this.player.isStopped),
    });
  }

  _playPause() {
    this.player.playPause((err, playing) => {
      if (err) {
        this.setState({
          error: err.message
        });
      }
      this._updateState();
    });
  }

  _base64ToArrayBuffer(base64) {
      var binary_string =  window.atob(base64);
      var len = binary_string.length;
      var bytes = new Uint8Array( len );
      for (var i = 0; i < len; i++)        {
          bytes[i] = binary_string.charCodeAt(i);
      }
      return bytes.buffer;
  }

  _stop() {
    this.player.stop(() => {
      this._updateState();

      RNFetchBlob.fs.readFile('/data/user/0/com.voicepay_app/files/' + filename, 'base64')
      .then((data) => {
         arrayBuffer = this._base64ToArrayBuffer(data);
         dataView = new DataView(arrayBuffer)
         avs.sendAudio(dataView)
      })
    });
  }

  _seek(percentage) {
    if (!this.player) {
      return;
    }

    this.lastSeek = Date.now();

    let position = percentage * this.player.duration;

    this.player.seek(position, () => {
      this._updateState();
    });
  }

  _reloadPlayer() {
    if (this.player) {
      this.player.destroy();
    }

    this.player = new Player(filename, {
      autoDestroy: false
    }).prepare((err) => {
      if (err) {
        console.log('error at _reloadPlayer():');
        console.log(err);
      } else {
        this.player.looping = this.state.loopButtonStatus;
      }

      this._updateState();
    });

    this._updateState();

    this.player.on('ended', () => {
      this._updateState();
    });
    this.player.on('pause', () => {
      this._updateState();
    });
  }

  _reloadRecorder() {
    if (this.recorder) {
      this.recorder.destroy();
    }

    this.recorder = new Recorder(filename, {
      bitrate: 256000,
      channels: 1,
      sampleRate: 16000,
      quality: 'max'
      //format: 'ac3', // autodetected
      //encoder: 'aac', // autodetected
    });

    console.log(this.recorder)

    this._updateState();
  }

  _toggleRecord() {
    if (this.player) {
      this.player.destroy();
    }

    this.recorder.toggleRecord((err, stopped) => {
      if (err) {
        this.setState({
          error: err.message
        });
      }
      if (stopped) {
        this._reloadPlayer();
        this._reloadRecorder();
      }

      this._updateState();
    });
  }

  _toggleLooping(value) {
    this.setState({
      loopButtonStatus: value
    });
    if (this.player) {
      this.player.looping = value;
    }
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
        <View style={{flex:1}}>
          <Text style={styles.title}>
            Playback
          </Text>
        </View>
        <View style={styles.buttonContainer}>
          <Button title={this.state.playPauseButton} disabled={this.state.playButtonDisabled} style={styles.button} onPress={() => this._playPause()}>
          </Button>
          <Button  title="Stop" disabled={this.state.stopButtonDisabled} style={styles.button} onPress={() => this._stop()}>
          </Button>
        </View>
        <View style={styles.settingsContainer}>
          <Switch
          onValueChange={(value) => this._toggleLooping(value)}
          value={this.state.loopButtonStatus} />
          <Text>Toggle Looping</Text>
        </View>
        <View style={styles.slider}>
          <Slider step={0.0001} disabled={this.state.playButtonDisabled} onValueChange={(percentage) => this._seek(percentage)} value={this.state.progress}/>
        </View>
        <View>
          <Text style={styles.title}>
            Recording
          </Text>
        </View>
        <View style={styles.buttonContainer}>
          <Button  title={this.state.recordButton} disabled={this.state.recordButtonDisabled} style={styles.button} onPress={() => this._toggleRecord()}>
          </Button>
        </View>
        <View>
          <Text style={styles.errorMessage}>{this.state.error}</Text>
        </View>
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
  button: {
    padding: 20,
    fontSize: 20,
    backgroundColor: 'white',
  },
  slider: {
    height: 10,
    margin: 10,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  settingsContainer: {
    flex: 1,
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  audiocontainer: {
    borderRadius: 4,
    borderWidth: 0.5,
    borderColor: '#d6d7da',
  },
  title: {
    fontSize: 19,
    fontWeight: 'bold',
    textAlign: 'center',
    padding: 20,
  },
  errorMessage: {
    fontSize: 15,
    textAlign: 'center',
    padding: 10,
    color: 'red'
  }
});

AppRegistry.registerComponent('voicepay_app', () => voicepay_app);
