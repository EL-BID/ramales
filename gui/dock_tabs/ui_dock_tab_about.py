from PyQt5.QtWidgets import QVBoxLayout, QLabel, QGridLayout
from qgis.PyQt.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QLocale

from .base.ui_dock_tab_base import DockTab


class DockTabAbout(DockTab):
    def __init__(self, dock):
        super().__init__(dock)

    def tab_start_ui(self):
        version = self.utils.get_metadata_value('version')
        gridLayoutAbout = QGridLayout()
        lb_msg = QLabel(self.tr('SaniHUB Ramales'))
        lb_msg.setFont(QFont('Arial', 15, QFont.Bold))
        # lb_msg.setWordWrap(True)
        gridLayoutAbout.addWidget(lb_msg, 0, 3, Qt.AlignHCenter)
        lb_img_bid = QLabel()
        pix_bid = QPixmap(':/plugins/tratamientos_descentralizados/icons/BID.png')
        lb_img_bid.setPixmap(pix_bid.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gridLayoutAbout.addWidget(lb_img_bid, 0, 0)
        lb_img_ufba = QLabel()
        pix_ufba = QPixmap(':/plugins/tratamientos_descentralizados/icons/UFBA.png')
        lb_img_ufba.setPixmap(pix_ufba.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gridLayoutAbout.addWidget(lb_img_ufba, 0, 2)
        lb_img_sanihub = QLabel()
        pix_sanihub = QPixmap(':/plugins/tratamientos_descentralizados/icons/saniHub.png')
        lb_img_sanihub.setPixmap(pix_sanihub.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        gridLayoutAbout.addWidget(lb_img_sanihub, 0, 1)

        lb_notice = QLabel(self.tr('Software livre para auxiliar no traçado e elaboração de projetos de ramais '
                                   'domiciliares de esgoto.'))
        lb_notice.setWordWrap(True)
        lb_notice.setAlignment(Qt.AlignHCenter)
        lb_notice.setFont(self.utils.formatItalicText())
        lb_notice.setMinimumHeight(50)
        gridLayoutAbout.addWidget(lb_notice, 1, 0, 1, 0, Qt.AlignCenter)

        lb_version = QLabel(self.tr('SaniHUB Ramales - Versão') + ' ' + version)
        lb_version.setWordWrap(True)
        gridLayoutAbout.addWidget(lb_version, 2, 0, 1, 0)

        loc = QLocale()
        lb_local = QLabel(self.tr('Local: ' + loc.nativeCountryName() +
                                  ' - Idioma: ' + loc.name()))
        gridLayoutAbout.addWidget(lb_local, 3, 0, 1, 0)
        lb_quick_guide = QLabel()
        urlLink = "<a href=\'https://www.iadb.org/'> www.iadb.org </a>"
        lb_quick_guide.setText(self.tr('Guia Rápido disponivel em ') + urlLink)
        lb_quick_guide.setOpenExternalLinks(True)
        # gridLayoutAbout.addWidget(lb_quick_guide, 4, 0, 1, 0)

        lb_financed = QLabel()
        lb_financed.setText(self.tr('O SaniHUB Ramales é um software livre que tem como objetivo auxiliar no traçado '
                                    'e na elaboração de projetos de ramais domiciliares de esgoto, com ferramentas '
                                    'para projeto de sistemas do tipo condominial ou convencionais. O Plug-in permite '
                                    'a elaboração de projetos a partir de informações coletadas em campo utilizando '
                                    'um formulário para a aplicação Qfield e processamento final no ambiente do Qgis.\n'
                                    'O software foi financiado pelo Banco Interamericano de Desenvolvimento (BID), '
                                    'com apoio da Agencia Espanhola de cooperação Internacional para o desenvolvimento '
                                    '(AECID) e da União Europeia (UE) , com a finalidade de promover o livre acesso a '
                                    'ferramentas modernas para o projeto de sistemas de esgoto e para o desenvolvimento '
                                    'de estratégias para assegurar serviços de saneamento em assentamentos informais, '
                                    'com recursos do Fundo Espanhol de Cooperação para Água y Saneamento na América '
                                    'Latina y el Caribe (FECASACL).'))
        lb_financed.setWordWrap(True)
        # lb_financed.setFont(QFont('Arial', 8))
        lb_financed.setAlignment(Qt.AlignJustify)
        # lb_financed.setMinimumHeight(220)
        gridLayoutAbout.addWidget(lb_financed, 5, 0, 1, 0)

        lb_team = QLabel()
        lb_team.setText(self.tr('Autores'))
        lb_team.setFont(self.utils.formatBoldText())
        lb_team.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_team, 6, 0, 1, 0)

        lb_team_str = QLabel()
        lb_team_str.setText(self.tr('Analista de Conceito:') + ' Ivan Paiva' +
                            '\n' + self.tr('Desenvolvedores:') + ' Dagoberto Medeiros e Fredson Menezes' +
                            '\n' + self.tr('Cálculos e modelagem:') + 'Ivan Paiva e Flávia Rebouças')
        # lb_team_ufba.setFont(QFont('Arial', 8))
        lb_team_str.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_team_str, 7, 0, 1, 0)

        lb_licence_tit = QLabel()
        lb_licence_tit.setText(self.tr('Licença'))
        lb_licence_tit.setFont(self.utils.formatBoldText())
        lb_licence_tit.setAlignment(Qt.AlignHCenter)
        gridLayoutAbout.addWidget(lb_licence_tit, 8, 0, 1, 0)

        lb_licence = QLabel()
        lb_licence.setText(self.tr('O SaniHUB Ramales é um software Copyleft. Possui código-fonte livre para '
                                   'atualizações e melhorias, assegurando, porém, que os produtos derivados da versão '
                                   'aqui disponível estejam licenciados sob termos idênticos, sendo vetada qualquer '
                                   'tipo de comercialização dos mesmos. \nTermos de Licença: GNU GPLv3 \nPara mais '
                                   'detalhes acesse o link de LICENÇA do plugin.'))
        lb_licence.setWordWrap(True)
        # lb_licence.setFont(QFont('Arial', 8))
        lb_licence.setAlignment(Qt.AlignJustify)
        gridLayoutAbout.addWidget(lb_licence, 9, 0, 1, 0)
        # gridLayoutAbout.setVerticalSpacing(25)

        # gridLayoutAbout.addStretch()
        self.setLayout(gridLayoutAbout)
