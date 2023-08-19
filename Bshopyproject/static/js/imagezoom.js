(function(window, $) {
    function ImgZoom(options) {
        this.opts = options;
        this.$el = options.$el;
        this.$sImg = options.$el.find('img');
        this.$zoomDiv = null;
        this.$bigImg = null;
        this.boxWidth = options.boxWidth;
        this.boxHeight = options.boxHeight;
        this.imgWidth = 0;
        this.imgHeight = 0;
        this.$mask = null;
        this.maskWidth = 0;
        this.maskHeight = 0;
        this.elWidth = 0;
        this.elHeight = 0;
        this._init();
    }
    ImgZoom.prototype = {
        constructor: ImgZoom,
        _init: function() {
            this.$el.css('position', 'relative');
            this.bindEvent();
        },
        _createZoomDiv: function() {
            var boxWidth = this.boxWidth;
            var boxHeight = this.boxHeight;

            this.$zoomDiv || (this.$zoomDiv = $('<div/>'));
            var offset = this.$el.offset();
            var zoomDivLeft = offset.left / 1 + this.$el.outerWidth(true) / 1 + this.opts.marginLeft / 1;
            var zoomDivTop = offset.top / 1;
            this.$bigImg.css('position', 'absolute');
            this.$zoomDiv.append(this.$bigImg);
            this.$zoomDiv.css({
                position: 'absolute',
                left: zoomDivLeft,
                top: zoomDivTop,
                zIndex: 999,
                width: boxWidth,
                height: boxHeight,
                overflow: 'hidden',
                border: '1px solid #222',
                background: '#FFF'
            });
            $('body').append(this.$zoomDiv);
        },
        _createMask: function() {
            var boxWidth = this.boxWidth;
            var boxHeight = this.boxHeight;
            this.elWidth = this.$el.outerWidth(true);
            this.elHeight = this.$el.outerHeight(true);

            this.maskWidth = Math.ceil(boxWidth / this.imgWidth * this.elWidth);
            this.maskHeight = Math.ceil(boxHeight / this.imgHeight * this.elHeight);
            this.maskWidth > this.elWidth && (this.maskWidth = this.elWidth);
            this.maskHeight > this.elHeight && (this.maskHeight = this.elHeight);
            this.$mask || (this.$mask = $('<div/>'));
            this.$mask.css({
                position: 'absolute',
                background: 'rgba(255,255,255,.4)',
                width: this.maskWidth,
                height: this.maskHeight,
                cursor: 'move'
            });
            this.$el.append(this.$mask);
        },
        createHTML: function() {
            this._createZoomDiv();
            this._createMask();
        },
        bindEvent: function() {
            var _this = this;
            this.$el.on({
                'mouseenter': function() {
                    _this.flag = true;
                    var imgOrigin = _this.$sImg.attr(_this.opts.origin);
                    var img = new Image();
                    img.onload = function() {
                        if (_this.flag) {
                            _this.imgWidth = img.width;
                            _this.imgHeight = img.height;
                            _this.$bigImg = $(img);
                            _this.createHTML();
                            _this.flag = false;
                        }
                    }
                    img.src = imgOrigin;
                },
                'mouseleave': function() {
                    if (_this.flag) {
                        _this.flag = false;
                    } else {
                        _this.$zoomDiv && _this.$zoomDiv.remove();
                        _this.$mask && _this.$mask.remove();
                    }

                },
                'mousemove': function(e) {
                    if (!_this.$bigImg) {
                        return false;
                    }
                    var offset = _this.$el.offset();
                    var maskW = _this.maskWidth;
                    var maskH = _this.maskHeight;
                    var left = e.pageX - offset.left - Math.ceil(maskW / 2);
                    var top = e.pageY - offset.top - Math.ceil(maskH / 2);
                    var maxX = _this.elWidth - maskW;
                    var maxY = _this.elHeight - maskH;

                    left = left < 0 ? 0 : left;
                    top = top < 0 ? 0 : top;
                    left = left > maxX ? maxX : left;
                    top = top > maxY ? maxY : top;

                    var bigLeft = -left * _this.imgWidth / _this.elWidth;
                    var bigTop = -top * _this.imgHeight / _this.elHeight;

                    _this.$mask.css({
                        left: left,
                        top: top
                    });
                    _this.$bigImg.css({
                        left: bigLeft,
                        top: bigTop
                    });
                }
            });
        }
    };

    $.fn.imgZoom = function(options) {
        var defaults = {
            boxWidth: 360,
            boxHeight: 360,
            marginLeft: 5,
            origin: 'data-origin'
        };
        $.each(this, function(i, t) {
            var config = $.extend(defaults, options);
            config.$el = $(t);
            new ImgZoom(config);
        });
    };
})(window, jQuery);