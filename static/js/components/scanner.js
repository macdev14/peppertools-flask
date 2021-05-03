import React from 'react'
import QrReader from 'react-qr-reader'


export default class Scanner extends React.Component {
   constructor(props){
        super(props);
        this.state = {
        result: 'No result'
        }
   }
  handleScan(data) {
    if (data) {
      this.setState({
        result: data
      })
    }
  }
  handleError(err) {
    return ''
  }
  render() {
    var that= this;
    return (
      <div>
        <QrReader
          delay={1500}
          onError={that.handleError}
          onScan={that.handleScan}
          style={{ width: '100%' }}
        />
       
      </div>
    )
  }
}
 