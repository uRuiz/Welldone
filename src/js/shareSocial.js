'use strict'

var shareSocial = shareSocial || {}

shareSocial = (function () {
  var self = {
    url: undefined,
    text: undefined,
    init: function () {
      document.dispatchEvent(new Event('shareSocial:ready'))
    },
    load: function () {
      this.attachedEvents()
    },
    attachedEvents: function () {
      document.querySelector('.fa-twitter-square').addEventListener('click', this.shareOnTwitter)
      document.querySelector('.fa-facebook-square').addEventListener('click', this.shareOnFacebook)
    },
    shareOnTwitter: function () {
      window.open(`http://twitter.com/share?text=${self.title}&url=${self.url}`, 'tshare', 'height=400,width=550,resizable=1,toolbar=0,menubar=0,status=0,location=0')
    },
    shareOnFacebook: function () {
      window.open(`https://www.facebook.com/share.php?u=${self.url}&title=${self.title}`, 'fbshare', 'height=380,width=660,resizable=0,toolbar=0,menubar=0,status=0,location=0,scrollbars=0')
    }
    
  }
  return self
}())

document.addEventListener('DOMContentLoaded', function () {
  shareSocial.init()
})