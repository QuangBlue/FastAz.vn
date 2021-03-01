class Style:

    style_bt = (
    """
    QPushButton {
        color: rgb(247, 247, 255); 
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid transparent;
        background-color: transparent;
        text-align: left;
        padding-left: 50px;
    }
    QPushButton[Active=true] {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid transparent;
        border-right: 5px solid rgb(85, 170, 255);
        background-color: transparent;
        text-align: left;
        padding-left: 50px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 18);
        border-left: 28px solid transparent;
    }
    QPushButton:pressed {
        background-color: rgb(85, 170, 255);
        border-left: 28px solid transparent;
    }
    """
    )

    main_light = """
   /* LINE EDIT */
    QLineEdit {
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 2px solid rgb(27, 29, 35);
        padding-left: 10px;
    }
    QLineEdit:hover {
        border: 2px solid rgb(64, 71, 88);
    }
    QLineEdit:focus {
        border: 2px solid rgb(91, 101, 124);
    }

    /* SCROLL BARS */
    QScrollBar:horizontal {
        border: none;
        background: rgb(225, 224, 226);
        height: 14px;
        margin: 0px 21px 0 21px;
        border-radius: 0px;
    }
    QScrollBar::handle:horizontal {
	background-color: rgb(65, 103, 192);
        min-width: 25px;
        border-radius: 7px
    }
    QScrollBar::add-line:horizontal {
        border: none;
        background: rgb(225, 224, 226);
        width: 20px;
        border-top-right-radius: 7px;
        border-bottom-right-radius: 7px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal {
        border: none;
        background: rgb(225, 224, 226);
        width: 20px;
        border-top-left-radius: 7px;
        border-bottom-left-radius: 7px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
    {
        background: none;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
    {
        background: none;
    }
    QScrollBar:vertical {
        border: none;
        background: rgb(225, 224, 226);
        width: 24px;
            margin: 21px 0 21px 8px;
        border-radius: 0px;
    }
    QScrollBar::handle:vertical {	
	background-color: rgb(65, 103, 192);
        min-height: 25px;
        border-radius: 7px
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: rgb(225, 224, 226);
        height: 20px;
        margin-left:8px;
        border-bottom-left-radius: 7px;
        border-bottom-right-radius: 7px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: rgb(225, 224, 226);
        height: 20px;
        margin-left:8px;
        border-top-left-radius: 7px;
        border-top-right-radius: 7px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    /* CHECKBOX */
    QCheckBox::indicator {
        border: 3px solid rgb(52, 59, 72);
        width: 15px;
        height: 15px;
        border-radius: 10px;
        background: rgb(44, 49, 60);
    }
    QCheckBox::indicator:hover {
        border: 3px solid rgb(58, 66, 81);
    }
    QCheckBox::indicator:checked {
        background: 3px solid rgb(52, 59, 72);
        border: 3px solid rgb(52, 59, 72);	
        background-image: url(:/icon/cil-check-alt.png);
    }

    /* RADIO BUTTON */
    QRadioButton::indicator {
        border: 3px solid rgb(52, 59, 72);
        width: 15px;
        height: 15px;
        border-radius: 10px;
        background: rgb(44, 49, 60);
    }
    QRadioButton::indicator:hover {
        border: 3px solid rgb(58, 66, 81);
    }
    QRadioButton::indicator:checked {
        background: 3px solid rgb(94, 106, 130);
        border: 3px solid rgb(52, 59, 72);	
    }

    /* COMBOBOX */
    QComboBox{
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 2px solid rgb(27, 29, 35);
        padding: 5px;
        padding-left: 40px;
        text-align: center;
    }
    QComboBox:hover{
        border: 2px solid rgb(64, 71, 88);
    }
    QComboBox::drop-down {

        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px; 
        border-left-width: 0px;
        border-left-color: rgba(39, 44, 54, 150);
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;	
        /*background-image: url(:/icon/cil-arrow-bottom.png);
        background-position: center;
        background-repeat: no-reperat;*/
    }
    QComboBox QAbstractItemView {
        text-align: center;
        background-image : none;
        color: rgb(85, 170, 255);	
        background-color: rgb(27, 29, 35);
        padding: 10px;
        selection-background-color: rgb(39, 44, 54);
    }

    /* SLIDERS */
    QSlider::groove:horizontal {
        border-radius: 9px;
        height: 18px;
        margin: 0px;
        background-color: rgb(52, 59, 72);
    }
    QSlider::groove:horizontal:hover {
        background-color: rgb(55, 62, 76);
    }
    QSlider::handle:horizontal {
        background-color: rgb(85, 170, 255);
        border: none;
        height: 18px;
        width: 18px;
        margin: 0px;
        border-radius: 9px;
    }
    QSlider::handle:horizontal:hover {
        background-color: rgb(105, 180, 255);
    }
    QSlider::handle:horizontal:pressed {
        background-color: rgb(65, 130, 195);
    }

    QSlider::groove:vertical {
        border-radius: 9px;
        width: 18px;
        margin: 0px;
        background-color: rgb(52, 59, 72);
    }
    QSlider::groove:vertical:hover {
        background-color: rgb(55, 62, 76);
    }
    QSlider::handle:vertical {
        background-color: rgb(85, 170, 255);
        border: none;
        height: 18px;
        width: 18px;
        margin: 0px;
        border-radius: 9px;
    }
    QSlider::handle:vertical:hover {
        background-color: rgb(105, 180, 255);
    }
    QSlider::handle:vertical:pressed {
        background-color: rgb(65, 130, 195);
    }

    QTableWidget {		
        background-color: rgb(254, 253, 255);
        padding: 10px;
        border-radius: 18px;
        gridline-color: rgb(254, 253, 255);
        color: rgb(84 84, 84);
    }
    QTableWidget::item{
        border-bottom : 1px solid rgb(220, 220,220);
        padding-left: 5px;
        padding-right: 5px;

    }
    QTableWidget::item:selected{
        background-color: rgb(85, 170, 255);
    }
    QHeaderView::section{
        Background-color: rgb(39, 44, 54);
        max-width: 30px;
        border: 1px solid rgb(44, 49, 60);
        border-style: none;
        border-bottom: 1px solid rgb(44, 49, 60);
        border-right: 1px solid rgb(44, 49, 60);
    }
    QTableWidget::horizontalHeader {	
        background-color: rgb(81, 255, 0);
    }
    QHeaderView::section:horizontal
    {
		border: none;
		border-bottom: 4px solid rgb(89, 125, 245);
		background-color: rgb(237, 237, 242);
		padding: 3px;
		border-top-left-radius: 7px;
		border-top-right-radius: 7px;
        	color: rgb(88, 88, 88);
    }
    QHeaderView::section:vertical
    {
        border: 1px solid rgb(44, 49, 60);
    }

    QPushButton {	
        border: none;
        background-color: transparent;
    }
    QPushButton:hover {
        background-color: rgb(89, 125, 245);
    }
    QPushButton:pressed {	
        background-color: rgb(85, 170, 255);
    }



    QFrame {
        color: rgb(84 84, 84);
    }

    #frame_main{
        background-color: rgb(237, 236, 238);

    }

    #frame_left_menu {
	background-color: rgb(59, 93, 176);
    }

    #frame_extra_menus{
	background-color: rgb(59, 93, 176);
    }

    #btn_toggle_menu {
	background-color: rgb(59, 93, 176);
    }
    #btn_toggle_menu:hover {
        background-color: rgb(89, 125, 245);
    }
    #btn_toggle_menu:pressed {	
        background-color: rgb(85, 170, 255);
    }
    #frame_label_top_btns{	
	background-color: rgb(73, 116, 220);

    }

    #frame_btns_right{	
	background-color: rgb(73, 116, 220);
    }

    #label_title_bar_top{	
        color: rgb(247, 247, 255);
    }

    #frame_top_info, #label_top_info_1 , #label_top_info_2 {
        border-bottom-width: 2px;	
        border-bottom-color: rgb(204, 203, 205);
        border-bottom-style: solid;	
        background: transparent;
    }

    #frame_grip{
	
	background-color: rgb(212, 211, 213);

    }

    #btn_theme{
        border-radius: 13px;
        margin-right: 10px;
        color: rgb(84 84, 84);
        background-color: rgb(232, 231, 234);
    }

    #btn_theme:hover{
        background-color: rgb(205, 204, 206);
    }

    #btn_theme:pressed{
        background-color: rgb(85, 170, 255);
        color: rgb(247, 247, 255);
    }
    #btn_minimize:hover, #btn_maximize_restore:hover, #btn_close:hover {
        background-color: rgb(109, 145, 245);
    } 

    #frameButtonChatBot{
	background-color: rgb(249, 248, 250);
	border-radius : 2px;
	margin : 5px;
    }

    #frameTitleOrderNew ,  #frameTitleOrderCancel,  #frameTitleOrderShipping, #frameTitleOrderSuccess, #frameTitleOrderReady {
        background-color: rgb(249, 248, 250);
        border-radius : 2px;
        margin-bottom: 10px;
    }

    QScrollArea{
        background-color: rgb(249, 248, 250);
        border-radius : 2px;
    }
    QPlainTextEdit{
        border: 1px solid  rgb(127, 126, 128);
        border-radius : 5px;
        padding : 12px;
        background-color: rgb(255, 255, 255);
        margin-bottom: 24px;
    }

        
    """
##############################
##############################
##############################
##############################
##############################

    main_dark = """
    /* LINE EDIT */
    QLineEdit {
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 2px solid rgb(27, 29, 35);
        padding-left: 10px;
    }
    QLineEdit:hover {
        border: 2px solid rgb(64, 71, 88);
    }
    QLineEdit:focus {
        border: 2px solid rgb(91, 101, 124);
    }

    /* SCROLL BARS */
    QScrollBar:horizontal {
        border: none;
        background: rgb(52, 59, 72);
        height: 14px;
        margin: 0px 21px 0 21px;
        border-radius: 0px;
    }
    QScrollBar::handle:horizontal {
        background: rgb(15, 170, 255);
        min-width: 25px;
        border-radius: 7px
    }
    QScrollBar::add-line:horizontal {
        border: none;
        background: rgb(55, 63, 77);
        width: 20px;
        border-top-right-radius: 7px;
        border-bottom-right-radius: 7px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:horizontal {
        border: none;
        background: rgb(55, 63, 77);
        width: 20px;
        border-top-left-radius: 7px;
        border-bottom-left-radius: 7px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
    {
        background: none;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
    {
        background: none;
    }
    QScrollBar:vertical {
        border: none;
        background: rgb(55, 63, 77);
        width: 24px;
            margin: 21px 0 21px 8px;
        border-radius: 0px;
    }
    QScrollBar::handle:vertical {	
        background: rgb(85, 170, 255);
        min-height: 25px;
        border-radius: 7px
    }
    QScrollBar::add-line:vertical {
        border: none;
        background: rgb(55, 63, 77);
        height: 20px;
        margin-left:8px;
        border-bottom-left-radius: 7px;
        border-bottom-right-radius: 7px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        border: none;
        background: rgb(55, 63, 77);
        height: 20px;
        margin-left:8px;
        border-top-left-radius: 7px;
        border-top-right-radius: 7px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    /* CHECKBOX */
    QCheckBox::indicator {
        border: 3px solid rgb(52, 59, 72);
        width: 15px;
        height: 15px;
        border-radius: 10px;
        background: rgb(44, 49, 60);
    }
    QCheckBox::indicator:hover {
        border: 3px solid rgb(58, 66, 81);
    }
    QCheckBox::indicator:checked {
        background: 3px solid rgb(52, 59, 72);
        border: 3px solid rgb(52, 59, 72);	
        background-image: url(:/icon/cil-check-alt.png);
    }

    /* RADIO BUTTON */
    QRadioButton::indicator {
        border: 3px solid rgb(52, 59, 72);
        width: 15px;
        height: 15px;
        border-radius: 10px;
        background: rgb(44, 49, 60);
    }
    QRadioButton::indicator:hover {
        border: 3px solid rgb(58, 66, 81);
    }
    QRadioButton::indicator:checked {
        background: 3px solid rgb(94, 106, 130);
        border: 3px solid rgb(52, 59, 72);	
    }

    /* COMBOBOX */
    QComboBox{
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 2px solid rgb(27, 29, 35);
        padding: 5px;
        padding-left: 40px;
        text-align: center;
    }
    QComboBox:hover{
        border: 2px solid rgb(64, 71, 88);
    }
    QComboBox::drop-down {

        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px; 
        border-left-width: 0px;
        border-left-color: rgba(39, 44, 54, 150);
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;	
        /*background-image: url(:/icon/cil-arrow-bottom.png);
        background-position: center;
        background-repeat: no-reperat;*/
    }
    QComboBox QAbstractItemView {
        text-align: center;
        background-image : none;
        color: rgb(85, 170, 255);	
        background-color: rgb(27, 29, 35);
        padding: 10px;
        selection-background-color: rgb(39, 44, 54);
    }

    /* SLIDERS */
    QSlider::groove:horizontal {
        border-radius: 9px;
        height: 18px;
        margin: 0px;
        background-color: rgb(52, 59, 72);
    }
    QSlider::groove:horizontal:hover {
        background-color: rgb(55, 62, 76);
    }
    QSlider::handle:horizontal {
        background-color: rgb(85, 170, 255);
        border: none;
        height: 18px;
        width: 18px;
        margin: 0px;
        border-radius: 9px;
    }
    QSlider::handle:horizontal:hover {
        background-color: rgb(105, 180, 255);
    }
    QSlider::handle:horizontal:pressed {
        background-color: rgb(65, 130, 195);
    }

    QSlider::groove:vertical {
        border-radius: 9px;
        width: 18px;
        margin: 0px;
        background-color: rgb(52, 59, 72);
    }
    QSlider::groove:vertical:hover {
        background-color: rgb(55, 62, 76);
    }
    QSlider::handle:vertical {
        background-color: rgb(85, 170, 255);
        border: none;
        height: 18px;
        width: 18px;
        margin: 0px;
        border-radius: 9px;
    }
    QSlider::handle:vertical:hover {
        background-color: rgb(105, 180, 255);
    }
    QSlider::handle:vertical:pressed {
        background-color: rgb(65, 130, 195);
    }
    QTableWidget {	
        background-color: rgb(40, 44, 52);
        padding: 10px;
        border-radius: 18px;
        gridline-color: rgb(40, 44, 52);

    }
    QTableWidget::item{
		border-bottom : 1px solid rgb(64, 69, 80);
        padding-left: 5px;
        padding-right: 5px;
    }
    QTableWidget::item:selected{
        background-color: rgb(85, 170, 255);
    }
    QHeaderView::section{
        Background-color: rgb(39, 44, 54);
        max-width: 30px;
        border: 1px solid rgb(44, 49, 60);
        border-style: none;
        border-bottom: 1px solid rgb(44, 49, 60);
        border-right: 1px solid rgb(44, 49, 60);
    }
    QTableWidget::horizontalHeader {	
        background-color: rgb(81, 255, 0);
    }
    QHeaderView::section:horizontal
    {

        border: 1px solid rgb(32, 34, 42);
        background-color: rgb(27, 29, 35);
        padding: 3px;
        border-top-left-radius: 7px;
        border-top-right-radius: 7px;
    }
    QHeaderView::section:vertical
    {
        border: 1px solid rgb(44, 49, 60);
    }

    QPushButton {	
        border: none;
        background-color: transparent;
    }
    QPushButton:hover {
        background-color: rgb(89, 125, 245);
    }
    QPushButton:pressed {	
        background-color: rgb(85, 170, 255);
    }

    QFrame {
        color: rgb(210, 210, 210);
    }

    #frame_main{
        background-color: rgb(40, 44, 52);
    }

    #stackedWidget {
    background: transparent;
    }

    #frame_left_menu {
        background-color: rgb(27, 29, 35);
    }

    #frame_extra_menus{
        background-color: rgb(27, 29, 35);
    }

    #btn_toggle_menu {
        background-color: rgb(27, 29, 35);
    }
    #btn_toggle_menu:hover {
        background-color: rgb(89, 125, 245);
    }
    #btn_toggle_menu:pressed {	
        background-color: rgb(85, 170, 255);
    }
    #frame_label_top_btns{	
        background-color: rgba(33, 37, 43, 150);

    }

    #frame_btns_right{	
        background-color: rgba(33, 37, 43, 150);
    }

    #label_title_bar_top, #label_credits, #label_version{	
        color: rgb(247, 247, 255);
    }

    #frame_top_info, #label_top_info_1 , #label_top_info_2 {
        border-bottom-width: 2px;	
        border-bottom-color: rgb(204, 203, 205);
        border-bottom-style: solid;	
        background: transparent;
    }

    #frame_grip{
        background-color: rgb(33, 37, 43);
        color: rgb(200, 199, 201);
    }

    #btn_theme{
        border-radius: 13px;
        margin-right: 10px;
        color: rgb(84 84, 84);
        background-color: rgb(232, 231, 234);
    }

    #btn_theme:hover{
        background-color: rgb(205, 204, 206);
    }

    #btn_theme:pressed{
        background-color: rgb(85, 170, 255);
        color: rgb(247, 247, 255);
    }
    #btn_minimize:hover, #btn_maximize_restore:hover, #btn_close:hover {
        background-color: rgb(109, 145, 245);
    }

        #frameButtonChatBot{
	background-color: rgb(37, 41, 49);
	border-radius : 2px;
	margin : 5px;
    }

    #frameTitleOrderNew ,  #frameTitleOrderCancel,  #frameTitleOrderShipping, #frameTitleOrderSuccess, #frameTitleOrderReady {
        background-color: rgb(37, 41, 49);
        border-radius : 2px;
        margin-bottom: 10px;
    }

    QScrollArea{
        background-color: rgb(37, 41, 49);
        border-radius : 2px;
    }

    QPlainTextEdit{

        border-radius : 5px;
        padding : 12px;
       background-color: rgb(47, 51, 59);
        margin-bottom: 24px;
    }

    """
##############################
################################################################
################################################################################################################
################################################################
    rating_dark = """
    QWidget{
    color: rgb(210, 210, 210);
    background-color: rgb(40, 44, 52);
    }
    QPlainTextEdit {
        background-color: rgb(39, 44, 54);
        border-radius: 5px;
        border: 2px solid rgb(27, 29, 35);
        padding-left: 10px;
    }
    QPlainTextEdit:hover {
        border: 2px solid rgb(64, 71, 88);
    }
    QPlainTextEdit:focus {
        border: 2px solid rgb(91, 101, 124);
    }

    /* COMBOBOX */
    QComboBox{
        background-color: rgb(27, 29, 35);
        border-radius: 5px;
        border: 2px solid rgb(27, 29, 35);
        padding: 5px;
        padding-left: 10px;
    }
    QComboBox:hover{
        border: 2px solid rgb(64, 71, 88);
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 40px; 
        border-left-width: 3px;
        border-left-color: rgba(39, 44, 54, 150);
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;	
        background-image: url(:/icon/cil-chevron-bottom.png);
        background-position: center;
        background-repeat: no-reperat;
    }
    QComboBox QAbstractItemView {
        color: rgb(85, 170, 255);	
        background-color: rgb(27, 29, 35);
        padding: 10px;
        selection-background-color: rgb(39, 44, 54);
    }
    #btn_send{
        border-radius: 25px;
        padding:8px 25px 7px 25px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));
        color: rgb(255, 255, 255);
    }

    #btn_send:hover{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 181, 253, 255), stop:1 rgba(89, 64, 231, 255));
    }

    #btn_send:pressed{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));
    }

    """
################################################################
################################################################
################################################################
################################################################
    rating_light = """
    QWidget{
	color: rgb(75, 75, 75);
    background-color: rgb(237, 236, 238);
    }
    QPlainTextEdit {
        background-color: rgb(237, 236, 238);
        border-radius: 5px;
        border: 2px solid rrgb(64, 71, 88);
        padding-left: 10px;
    }
    QPlainTextEdit:hover {
        border: 2px solid rgb(64, 71, 88);
    }
    QPlainTextEdit:focus {
        border: 2px solid rgb(89, 125, 245);
    }

    /* COMBOBOX */
    QComboBox{
        background-color: rgb(89, 125, 245);
        border-radius: 5px;
        border: 2px solid rgb(89, 105, 245);
        padding: 5px;
        padding-left: 10px;
        color: rgb(247, 245, 248);
    }
    QComboBox:hover{
        border: 2px solid rgb(69, 65, 245);
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 40px; 
        border-left-width: 3px;
        border-left-color: rgb(237, 236, 238);
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;	
        background-image: url(:/icon/cil-chevron-bottom.png);
        background-position: center;
        background-repeat: no-reperat;
    }
    QComboBox QAbstractItemView {
        color: rgb(75, 75, 75);
        background-color: rgb(89, 125, 245);
        padding: 10px;
        selection-background-color: rgb(39, 44, 54);
    }
    #btn_send{
        border-radius: 25px;
        padding:8px 25px 7px 25px;
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));
        color: rgb(255, 255, 255);
    }

    #btn_send:hover{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 181, 253, 255), stop:1 rgba(89, 64, 231, 255));
    }

    #btn_send:pressed{
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));
    }

    """