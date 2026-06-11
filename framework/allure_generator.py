import os
import shutil
import sys
from io import StringIO

import allure_combine
from bs4 import BeautifulSoup as BS

import logging

from framework import common, path


def output_allure_html():
    """
    整合allure result，並匯出帶有時間標記的獨立的allure html報告
    """

    # xdist 變更時間戳與絕對路徑取得方式
    TIMESTAMP = common.read_txt_by(path.Base.TIMESTAMP_TXT)
    ALLURE = common.read_txt_by(path.Base.ALLURE_PATH_TXT)
    logging.info(f'🟢 ALLURE: {ALLURE}')
    
    # 整合 allure_tmp 為 allure_index 資料夾，其中包含 index.html 報告
    try:
        os.system(f'{ALLURE} generate {path.Reports.ALLURE_TMP} --clean -o {path.Reports.ALLURE_INDEX}')
        logging.info(f'✅ 成功: 已整合 tmp_dir 為新的 index_dir: {path.Reports.ALLURE_INDEX}')
    except Exception as e:
        logging.error(f'❌ 失敗: 未整合 tmp_dir 為新的 index_dir: {path.Reports.ALLURE_INDEX}\n{e}')

    # 整合 allure_index 內的 index.html 並在其中生成獨立報告 complete.html
    try:
        # logging.info(f'🔄 開始生成 Allure HTML 報告...')
        # old_stdout = sys.stdout
        # sys.stdout = StringIO()
        allure_combine.combine_allure(path.Reports.ALLURE_INDEX)
        # sys.stdout = old_stdout
        logging.info(f'✅ 成功: 已生成 complete.html 於 index_dir: {path.Reports.ALLURE_INDEX}')
    except Exception as e:
        # sys.stdout = old_stdout
        logging.error(f'❌ 失敗: 未生成 complete.html 於 index_dir: {path.Reports.ALLURE_INDEX}\n{e}')
        logging.warning(f'🟡 請確認 allure commandline 版本介於 2.21.0 和 2.22.0 之間')

    # 移動 complete.html 到附加時間戳的資料夾
    try:
        # xdist: 同動態變數問題，於此處再標記時間戳
        REPORTS_TIMESTAMP = os.path.join(path.REPORTS, TIMESTAMP)
        os.makedirs(REPORTS_TIMESTAMP, exist_ok=True)
        # 將 complete.html 移到時間戳資料夾內並改名
        src_complete = os.path.join(path.Reports.ALLURE_INDEX, 'complete.html')
        expand_screenshot(src_complete)
        dst_complete = os.path.join(REPORTS_TIMESTAMP, f'allure_{TIMESTAMP}.html')
        os.rename(src_complete, dst_complete)
        # 將 image 資料夾移到時間戳資料夾內
        src_image = path.Reports.IMAGE
        dst_image = os.path.join(REPORTS_TIMESTAMP, 'image')
        os.rename(src_image, dst_image)
        logging.info(f'✅ 成功: 已移動 complete.html 到資料夾: {path.REPORTS}')
        logging.info(f'✅ 成功: 已修改 complete.html 檔案名為: allure_{TIMESTAMP}.html')
    except Exception as e:
        logging.error('❌ 失敗: 請確認 最終report路徑 及 展開截圖的設定 是否有誤')

    # 移除不需要的 allure 暫存檔和資料夾
    try:
        # 可都不用移除tmp，CI直接於 sysargs 使用 --clean-alluredir 即可。
        shutil.rmtree(path.Reports.ALLURE_INDEX, ignore_errors=True)
        logging.info(f'✅ 成功: 已移除 index_dir: {path.Reports.ALLURE_INDEX}')
    except Exception as e:
        logging.error(f'❌ 失敗: 移除 index_dir 時發生錯誤，請確認路徑是否正確')


def expand_screenshot(file_path):
    """
    修改allure report讓截圖能自動開啟
    """
    old_text = '<div class="attachment-row__content \'+u(o(n(3735)).call(c,"attachment",null!=e?h(e,"uid"):e,{name:"b",hash:{},data:a,loc:{start:{line:30,column:44},end:{line:30,column:67}}}))+\'\"></div>\\n    </div>\\n</div>\\n\''
    new_text = '<div class="attachment-row__content \'+u(o(n(3735)).call(c,"attachment",null!=e?h(e,"uid"):e,{name:"b",hash:{},data:a,loc:{start:{line:30,column:44},end:{line:30,column:67}}}))+\'\">   <div class=\"attachment\">    <div class=\"attachment__media-container\"><img class=\"attachment__media\"  onerror=\"imageError(this)\" src=\"data/attachments/\'+u(l(null!=e?h(e,\"source\"):e,e))+\'\"/> </div>\\n</div>\\n</div>\\n   </div>\\n</div>\''

    old_dom = '''document.addEventListener("DOMContentLoaded", function() {
            var old_prefilter = jQuery.htmlPrefilter;

            jQuery.htmlPrefilter = function(v) {
            
                var regs = [
                    /<a[^>]*href="(?<url>[^"]*)"[^>]*>/gi,
                    /<img[^>]*src="(?<url>[^"]*)"\/?>/gi,
                    /<source[^>]*src="(?<url>[^"]*)"/gi
                ];
                
                var replaces = {};

                for (i in regs)
                {
                    reg = regs[i];

                    var m = true;
                    var n = 0;
                    while (m && n < 100)
                    {
                        n += 1;
                        
                        m = reg.exec(v);
                        if (m)
                        {
                            if (m['groups'] && m['groups']['url'])
                            {
                                var url = m['groups']['url'];
                                if (server_data.hasOwnProperty(url))
                                {
                                    console.log(`Added url:${url} to be replaced with data of ${server_data[url].length} bytes length`);
                                    replaces[url] = server_data[url];                                    
                                }
                            }
                        }
                    }
                }
                
                for (let src in replaces)
                {
                    let dest = replaces[src];
                    v = v.replace(src, dest);
                }

                return old_prefilter(v);
            };
        });'''

    new_dom = '''document.addEventListener("DOMContentLoaded", function() {
            var old_prefilter = jQuery.htmlPrefilter;

            jQuery.htmlPrefilter = function(v) {
            
                var regs = [
                    /<a[^>]*href="(?<url>[^"]*)"[^>]*>/gi,
                    /<img[^>]*src="(?<url>[^"]*)"\/?>/gi,
                    /<source[^>]*src="(?<url>[^"]*)"/gi
                ];
                
                var replaces = {};

                for (i in regs)
                {
                    reg = regs[i];

                    var m = true;
                    var n = 0;
                    while (m && n < 500)
                    {
                        n += 1;
                        
                        m = reg.exec(v);
                        if (m)
                        {
                            if (m['groups'] && m['groups']['url'])
                            {
                                var url = m['groups']['url'];
                                if (server_data.hasOwnProperty(url))
                                {
                                    console.log(`Added url:${url} to be replaced with data of ${server_data[url].length} bytes length`);
                                    replaces[url] = server_data[url];  
                                    v = v.replace(url, replaces[url]);                                  
                                }
                            }
                        }
                    }
                }
                
                

                return old_prefilter(v);
            };
        });'''

    old_js = '''<script>(function () {
    var settings = allure.getPluginSettings('screen-diff', { diffType: 'diff' });

    function renderImage(src) {
        return (
            '<div class="screen-diff__container">' +
            '<img class="screen-diff__image" src="' +
            src +
            '">' +
            '</div>'
        );
    }

    function findImage(data, name) {
        if (data.testStage && data.testStage.attachments) {
            var matchedImage = data.testStage.attachments.filter(function (attachment) {
                return attachment.name === name;
            })[0];
            if (matchedImage) {
                return 'data/attachments/' + matchedImage.source;
            }
        }
        return null;
    }

    function renderDiffContent(type, diffImage, actualImage, expectedImage) {
        if (type === 'diff') {
            if (diffImage) {
                return renderImage(diffImage);
            }
        }
        if (type === 'overlay' && expectedImage) {
            return (
                '<div class="screen-diff__overlay screen-diff__container">' +
                '<img class="screen-diff__image" src="' +
                expectedImage +
                '">' +
                '<div class="screen-diff__image-over">' +
                '<img class="screen-diff__image" src="' +
                actualImage +
                '">' +
                '</div>' +
                '</div>'
            );
        }
        if (actualImage) {
            return renderImage(actualImage);
        }
        return 'No diff data provided';
    }

    var TestResultView = Backbone.Marionette.View.extend({
        regions: {
            subView: '.screen-diff-view',
        },
        template: function () {
            return '<div class="screen-diff-view"></div>';
        },
        onRender: function () {
            var data = this.model.toJSON();
            var testType = data.labels.filter(function (label) {
                return label.name === 'testType';
            })[0];
            var diffImage = findImage(data, 'diff');
            var actualImage = findImage(data, 'actual');
            var expectedImage = findImage(data, 'expected');
            if (!testType || testType.value !== 'screenshotDiff') {
                return;
            }
            this.showChildView(
                'subView',
                new ScreenDiffView({
                    diffImage: diffImage,
                    actualImage: actualImage,
                    expectedImage: expectedImage,
                }),
            );
        },
    });
    var ErrorView = Backbone.Marionette.View.extend({
        templateContext: function () {
            return this.options;
        },
        template: function (data) {
            return '<pre class="screen-diff-error">' + data.error + '</pre>';
        },
    });
    var AttachmentView = Backbone.Marionette.View.extend({
        regions: {
            subView: '.screen-diff-view',
        },
        template: function () {
            return '<div class="screen-diff-view"></div>';
        },
        onRender: function () {
            jQuery
                .getJSON(this.options.sourceUrl)
                .then(this.renderScreenDiffView.bind(this), this.renderErrorView.bind(this));
        },
        renderErrorView: function (error) {
            console.log(error);
            this.showChildView(
                'subView',
                new ErrorView({
                    error: error.statusText,
                }),
            );
        },
        renderScreenDiffView: function (data) {
            this.showChildView(
                'subView',
                new ScreenDiffView({
                    diffImage: data.diff,
                    actualImage: data.actual,
                    expectedImage: data.expected,
                }),
            );
        },
    });

    var ScreenDiffView = Backbone.Marionette.View.extend({
        className: 'pane__section',
        events: function () {
            return {
                ['click [name="screen-diff-type-' + this.cid + '"]']: 'onDiffTypeChange',
                'mousemove .screen-diff__overlay': 'onOverlayMove',
            };
        },
        initialize: function (options) {
            this.diffImage = options.diffImage;
            this.actualImage = options.actualImage;
            this.expectedImage = options.expectedImage;
            this.radioName = 'screen-diff-type-' + this.cid;
        },
        templateContext: function () {
            return {
                diffType: settings.get('diffType'),
                diffImage: this.diffImage,
                actualImage: this.actualImage,
                expectedImage: this.expectedImage,
                radioName: this.radioName,
            };
        },
        template: function (data) {
            if (!data.diffImage && !data.actualImage && !data.expectedImage) {
                return '';
            }

            return (
                '<h3 class="pane__section-title">Screen Diff</h3>' +
                '<div class="screen-diff__content">' +
                '<div class="screen-diff__switchers">' +
                '<label><input type="radio" name="' +
                data.radioName +
                '" value="diff"> Show diff</label>' +
                '<label><input type="radio" name="' +
                data.radioName +
                '" value="overlay"> Show overlay</label>' +
                '</div>' +
                renderDiffContent(
                    data.diffType,
                    data.diffImage,
                    data.actualImage,
                    data.expectedImage,
                ) +
                '</div>'
            );
        },
        adjustImageSize: function (event) {
            var overImage = this.$(event.target);
            overImage.width(overImage.width());
        },
        onRender: function () {
            const diffType = settings.get('diffType');
            this.$('[name="' + this.radioName + '"][value="' + diffType + '"]').prop(
                'checked',
                true,
            );
            if (diffType === 'overlay') {
                this.$('.screen-diff__image-over img').on('load', this.adjustImageSize.bind(this));
            }
        },
        onOverlayMove: function (event) {
            var pageX = event.pageX;
            var containerScroll = this.$('.screen-diff__container').scrollLeft();
            var elementX = event.currentTarget.getBoundingClientRect().left;
            var delta = pageX - elementX + containerScroll;
            this.$('.screen-diff__image-over').width(delta);
        },
        onDiffTypeChange: function (event) {
            settings.save('diffType', event.target.value);
            this.render();
        },
    });
    allure.api.addTestResultBlock(TestResultView, { position: 'before' });
    allure.api.addAttachmentViewer('application/vnd.allure.image.diff', {
        View: AttachmentView,
        icon: 'fa fa-exchange',
    });
})();
</script>'''

    # new_js只比原本多個imageError function來處理沒有讀到圖片的情況
    new_js = '''<script>(function () {
    var settings = allure.getPluginSettings('screen-diff', { diffType: 'diff' });

    function renderImage(src) {
        return (
            '<div class="screen-diff__container">' +
            '<img class="screen-diff__image" src="' +
            src +
            '">' +
            '</div>'
        );
    }

    function findImage(data, name) {
        if (data.testStage && data.testStage.attachments) {
            var matchedImage = data.testStage.attachments.filter(function (attachment) {
                return attachment.name === name;
            })[0];
            if (matchedImage) {
                return 'data/attachments/' + matchedImage.source;
            }
        }
        return null;
    }

    function renderDiffContent(type, diffImage, actualImage, expectedImage) {
        if (type === 'diff') {
            if (diffImage) {
                return renderImage(diffImage);
            }
        }
        if (type === 'overlay' && expectedImage) {
            return (
                '<div class="screen-diff__overlay screen-diff__container">' +
                '<img class="screen-diff__image" src="' +
                expectedImage +
                '">' +
                '<div class="screen-diff__image-over">' +
                '<img class="screen-diff__image" src="' +
                actualImage +
                '">' +
                '</div>' +
                '</div>'
            );
        }
        if (actualImage) {
            return renderImage(actualImage);
        }
        return 'No diff data provided';
    }

    var TestResultView = Backbone.Marionette.View.extend({
        regions: {
            subView: '.screen-diff-view',
        },
        template: function () {
            return '<div class="screen-diff-view"></div>';
        },
        onRender: function () {
            var data = this.model.toJSON();
            var testType = data.labels.filter(function (label) {
                return label.name === 'testType';
            })[0];
            var diffImage = findImage(data, 'diff');
            var actualImage = findImage(data, 'actual');
            var expectedImage = findImage(data, 'expected');
            if (!testType || testType.value !== 'screenshotDiff') {
                return;
            }
            this.showChildView(
                'subView',
                new ScreenDiffView({
                    diffImage: diffImage,
                    actualImage: actualImage,
                    expectedImage: expectedImage,
                }),
            );
        },
    });
    var ErrorView = Backbone.Marionette.View.extend({
        templateContext: function () {
            return this.options;
        },
        template: function (data) {
            return '<pre class="screen-diff-error">' + data.error + '</pre>';
        },
    });
    var AttachmentView = Backbone.Marionette.View.extend({
        regions: {
            subView: '.screen-diff-view',
        },
        template: function () {
            return '<div class="screen-diff-view"></div>';
        },
        onRender: function () {
            jQuery
                .getJSON(this.options.sourceUrl)
                .then(this.renderScreenDiffView.bind(this), this.renderErrorView.bind(this));
        },
        renderErrorView: function (error) {
            console.log(error);
            this.showChildView(
                'subView',
                new ErrorView({
                    error: error.statusText,
                }),
            );
        },
        renderScreenDiffView: function (data) {
            this.showChildView(
                'subView',
                new ScreenDiffView({
                    diffImage: data.diff,
                    actualImage: data.actual,
                    expectedImage: data.expected,
                }),
            );
        },
    });

    var ScreenDiffView = Backbone.Marionette.View.extend({
        className: 'pane__section',
        events: function () {
            return {
                ['click [name="screen-diff-type-' + this.cid + '"]']: 'onDiffTypeChange',
                'mousemove .screen-diff__overlay': 'onOverlayMove',
            };
        },
        initialize: function (options) {
            this.diffImage = options.diffImage;
            this.actualImage = options.actualImage;
            this.expectedImage = options.expectedImage;
            this.radioName = 'screen-diff-type-' + this.cid;
        },
        templateContext: function () {
            return {
                diffType: settings.get('diffType'),
                diffImage: this.diffImage,
                actualImage: this.actualImage,
                expectedImage: this.expectedImage,
                radioName: this.radioName,
            };
        },
        template: function (data) {
            if (!data.diffImage && !data.actualImage && !data.expectedImage) {
                return '';
            }

            return (
                '<h3 class="pane__section-title">Screen Diff</h3>' +
                '<div class="screen-diff__content">' +
                '<div class="screen-diff__switchers">' +
                '<label><input type="radio" name="' +
                data.radioName +
                '" value="diff"> Show diff</label>' +
                '<label><input type="radio" name="' +
                data.radioName +
                '" value="overlay"> Show overlay</label>' +
                '</div>' +
                renderDiffContent(
                    data.diffType,
                    data.diffImage,
                    data.actualImage,
                    data.expectedImage,
                ) +
                '</div>'
            );
        },
        adjustImageSize: function (event) {
            var overImage = this.$(event.target);
            overImage.width(overImage.width());
        },
        onRender: function () {
            const diffType = settings.get('diffType');
            this.$('[name="' + this.radioName + '"][value="' + diffType + '"]').prop(
                'checked',
                true,
            );
            if (diffType === 'overlay') {
                this.$('.screen-diff__image-over img').on('load', this.adjustImageSize.bind(this));
            }
        },
        onOverlayMove: function (event) {
            var pageX = event.pageX;
            var containerScroll = this.$('.screen-diff__container').scrollLeft();
            var elementX = event.currentTarget.getBoundingClientRect().left;
            var delta = pageX - elementX + containerScroll;
            this.$('.screen-diff__image-over').width(delta);
        },
        onDiffTypeChange: function (event) {
            settings.save('diffType', event.target.value);
            this.render();
        },
    });
    allure.api.addTestResultBlock(TestResultView, { position: 'before' });
    allure.api.addAttachmentViewer('application/vnd.allure.image.diff', {
        View: AttachmentView,
        icon: 'fa fa-exchange',
    });
})();

function imageError(img){
    img.style.display ='none';
}
</script>'''

    # revise description html tag display issue
    pre_code_start_tag = '&lt;pre&gt;&lt;code&gt;'
    pre_code_end_tag = '&lt;/code&gt;&lt;/pre&gt;'
    p_start_tag = '&lt;p&gt;'
    p_end_tag = '&lt;/p&gt;'

    with open(file_path, 'r', encoding="utf-8") as f:
        soup = BS(f.read(), "html.parser")

    final_html = str(soup).replace(old_text, new_text).replace(old_dom, new_dom).replace(old_js, new_js)

    # revise description html tag display issue
    final_html = final_html.replace(pre_code_start_tag, '').replace(pre_code_end_tag, '').replace(p_start_tag,
                                                                                                  '').replace(p_end_tag,
                                                                                                              '')

    with open(file_path, "w", encoding="utf-8") as f_output:
        f_output.write(final_html)
