"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from urllib import response
import requests
from urllib.request import urlopen
from urllib.error import *
import logging
from decouple import config
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, Application

URL = 'https://countryflagsapi.com/png/'
TOKEN = config('TOKEN')
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

countries = ('united arab emirates', 'the united arab emirates', 'ae', 'are', '784', 'andorra', 'ad', 'and', '020',
             'afghanistan', 'af', 'afg', '004', 'antigua and barbuda', 'ag', 'atg', '028', 'anguilla', 'ai', 'aia',
             '660', 'albania', 'al', 'alb', '008', 'armenia', 'am', 'arm', '051', 'angola', 'ao', 'ago', '024',
             'antarctica', 'aq', 'ata', '010', 'argentina', 'ar', 'arg', '032', 'american samoa', 'as', 'asm', '016',
             'austria', 'at', 'aut', '040', 'australia', 'au', 'aus', '036', 'aruba', 'aw', 'abw', '533',
             'åland islands', 'ax', 'ala', '248', 'azerbaijan', 'az', 'aze', '031', 'bosnia and herzegovina', 'ba',
             'bih', '070', 'barbados', 'bb', 'brb', '052', 'bangladesh', 'bd', 'bgd', '050', 'belgium', 'be', 'bel',
             '056', 'burkina faso', 'bf', 'bfa', '854', 'bulgaria', 'bg', 'bgr', '100', 'bahrain', 'bh', 'bhr', '048',
             'burundi', 'bi', 'bdi', '108', 'benin', 'bj', 'ben', '204', 'saint barthélemy', 'bl', 'blm', '652',
             'bermuda', 'bm', 'bmu', '060', 'brunei darussalam', 'bn', 'brn', '096', 'bolivia', 'bo', 'bol', '068',
             'bonaire', 'bq', 'bes', '535', 'brazil', 'br', 'bra', '076', 'the bahamas', 'bs', 'bhs', '044', 'bhutan',
             'bt', 'btn', '064', 'bouvet island', 'bv', 'bvt', '074', 'botswana', 'bw', 'bwa', '072', 'belarus', 'by',
             'blr', '112', 'belize', 'bz', 'blz', '084', 'canada', 'ca', 'can', '124', 'the cocos islands', 'cc', 'cck',
             '166', 'democratic republic of congo', 'cd', 'cod', '180', 'the central african republic', 'cf', 'caf',
             '140', 'congo', 'cg', 'cog', '178', 'switzerland', 'ch', 'che', '756', "côte d'ivoire", 'ci', 'civ', '384',
             'the cook islands', 'ck', 'cok', '184', 'chile', 'cl', 'chl', '152', 'cameroon', 'cm', 'cmr', '120',
             'china', 'cn', 'chn', '156', 'colombia', 'co', 'col', '170', 'costa rica', 'cr', 'cri', '188', 'cuba',
             'cu', 'cub', '192', 'cabo verde', 'cv', 'cpv', '132', 'curaçao', 'cw', 'cuw', '531', 'christmas island',
             'cx', 'cxr', '162', 'cyprus', 'cy', 'cyp', '196', 'czechia', 'cz', 'cze', '203', 'germany', 'de', 'deu',
             '276', 'djibouti', 'dj', 'dji', '262', 'denmark', 'dk', 'dnk', '208', 'dominica', 'dm', 'dma', '212',
             'dominican republic', 'do', 'dom', '214', 'algeria', 'dz', 'dza', '012', 'ecuador', 'ec', 'ecu', '218',
             'estonia', 'ee', 'est', '233', 'egypt', 'eg', 'egy', '818', 'western sahara', 'eh', 'esh', '732',
             'eritrea', 'er', 'eri', '232', 'spain', 'es', 'esp', '724', 'ethiopia', 'et', 'eth', '231',
             'european union', 'the european union', 'europe', 'eu', 'eur', 'finland', 'fi', 'fin', '246', 'fiji', 'fj',
             'fji', '242', 'the falkland islands', 'fk', 'flk', '238', 'the federated states of micronesia',
             'micronesia', 'fm', 'fsm', '583', 'the faroe islands', 'fo', 'fro', '234', 'france', 'fr', 'fra', '250',
             'gabon', 'ga', 'gab', '266', 'england', 'gb-eng', 'gb-eng', 'northern ireland', 'gb-nir', 'gb-nir',
             'scotland', 'gb-sct', 'gb-sct', 'wales', 'gb-wls', 'gb-wls',
             'the united kingdom of great britain and northern ireland', 'great britain', 'united kingdom',
             'the united kingdom', 'gb', 'gbr', '826', 'grenada', 'gd', 'grd', '308', 'georgia', 'ge', 'geo', '268',
             'french guiana', 'gf', 'guf', '254', 'guernsey', 'gg', 'ggy', '831', 'ghana', 'gh', 'gha', '288',
             'gibraltar', 'gi', 'gib', '292', 'greenland', 'gl', 'grl', '304', 'gambia', 'gm', 'gmb', '270', 'guinea',
             'gn', 'gin', '324', 'guadeloupe', 'gp', 'glp', '312', 'equatorial guinea', 'gq', 'gnq', '226', 'greece',
             'gr', 'grc', '300', 'south georgia and the south sandwich islands', 'gs', 'sgs', '239', 'guatemala',
             'gt', 'gtm', '320', 'guam', 'gu', 'gum', '316', 'guinea-bissau', 'gw', 'gnb', '624', 'guyana', 'gy', 'guy',
             '328', 'hong kong', 'hk', 'hkg', '344', 'heard island and mcdonald islands', 'hm', 'hmd', '334',
             'honduras', 'hn', 'hnd', '340', 'croatia', 'hr', 'hrv', '191', 'croatia', 'hr', 'hrv', '191', 'haiti',
             'ht', 'hti', '332', 'hungary', 'hu', 'hun', '348', 'indonesia', 'id', 'idn', '360', 'ireland', 'ie', 'irl',
             '372', 'israel', 'il', 'isr', '376', 'isle of man', 'im', 'imn', '833', 'india', 'in', 'ind', '356',
             'the british indian ocean territory', 'io', 'iot', '086', 'iraq', 'iq', 'irq', '368', 'iran', 'ir', 'irn',
             '364', 'iceland', 'is', 'isl', '352', 'italy', 'it', 'ita', '380', 'jersey', 'je', 'jey', '832', 'jamaica',
             'jm', 'jam', '388', 'jordan', 'jo', 'jor', '400', 'japan', 'jp', 'jpn', '392', 'kenya', 'ke', 'ken', '404',
             'kyrgyzstan', 'kg', 'kgz', '417', 'cambodia', 'kh', 'khm', '116', 'kiribati', 'ki', 'kir', '296',
             'the comoros', 'km', 'com', '174', 'saint kitts and nevis', 'kn', 'kna', '659',
             "the democratic people's republic of korea", 'north korea', 'kp', 'prk', '408', 'the republic of korea',
             'southe korea', 'kr', 'kor', '410', 'kuwait', 'kw', 'kwt', '414', 'the cayman islands', 'ky', 'cym', '136',
             'kazakhstan', 'kz', 'kaz', '398', "the lao people's democratic republic", 'laos', 'la', 'lao', '418',
             'lebanon', 'lb', 'lbn', '422', 'saint lucia', 'lc', 'lca', '662', 'liechtenstein', 'li', 'lie', '438',
             'sri lanka', 'lk', 'lka', '144', 'liberia', 'lr', 'lbr', '430', 'lesotho', 'ls', 'lso', '426', 'lithuania',
             'lt', 'ltu', '440', 'luxembourg', 'lu', 'lux', '442', 'latvia', 'lv', 'lva', '428', 'libya', 'ly', 'lby',
             '434', 'morocco', 'ma', 'mar', '504', 'monaco', 'mc', 'mco', '492', 'the republic of moldova', 'moldova',
             'md', 'mda', '498', 'montenegro', 'me', 'mne', '499', 'saint martin', 'mf', 'maf', '663', 'madagascar',
             'mg', 'mdg', '450', 'the marshall islands', 'mh', 'mhl', '584', 'republic of north macedonia', 'mali',
             'ml', 'mli', '466', 'mk', 'mkd', '807', 'myanmar', 'mm', 'mmr', '104', 'mongolia', 'mn', 'mng', '496',
             'macao', 'mo', 'mac', '446', 'the northern mariana islands', 'mp', 'mnp', '580', 'martinique', 'mq', 'mtq',
             '474', 'mauritania', 'mr', 'mrt', '478', 'montserrat', 'ms', 'msr', '500', 'malta', 'mt', 'mlt', '470',
             'mauritius', 'mu', 'mus', '480', 'maldives', 'mv', 'mdv', '462', 'malawi', 'mw', 'mwi', '454', 'mexico',
             'mx', 'mex', '484', 'malaysia', 'my', 'mys', '458', 'mozambique', 'mz', 'moz', '508', 'namibia', 'na',
             'nam', '516', 'new caledonia', 'nc', 'ncl', '540', 'niger', 'ne', 'ner', '562', 'norfolk island', 'nf',
             'nfk', '574', 'nigeria', 'ng', 'nga', '566', 'nicaragua', 'ni', 'nic', '558', 'netherlands', 'nl', 'nld',
             '528', 'norway', 'no', 'nor', '578', 'nepal', 'np', 'npl', '524', 'nauru', 'nr', 'nru', '520', 'niue',
             'nu', 'niu', '570', 'new zealand', 'nz', 'nzl', '554', 'oman', 'om', 'omn', '512', 'panama', 'pa', 'pan',
             '591', 'peru', 'pe', 'per', '604', 'french polynesia', 'pf', 'pyf', '258', 'papua new guinea', 'pg', 'png',
             '598', 'philippines', 'ph', 'phl', '608', 'pakistan', 'pk', 'pak', '586', 'poland', 'pl', 'pol', '616',
             'saint pierre and miquelon', 'pm', 'spm', '666', 'pitcairn', 'pn', 'pcn', '612', 'puerto rico', 'pr',
             'pri', '630', 'palestine', 'ps', 'pse', '275', 'portugal', 'pt', 'prt', '620', 'palau', 'pw', 'plw', '585',
             'paraguay', 'py', 'pry', '600', 'qatar', 'qa', 'qat', '634', 'réunion', 're', 'reu', '638', 'romania',
             'ro', 'rou', '642', 'serbia', 'rs', 'srb', '688', 'russian federation', 'ru', 'rus', '643', 'rwanda', 'rw',
             'rwa', '646', 'saudi arabia', 'sa', 'sau', '682', 'solomon islands', 'sb', 'slb', '090', 'seychelles',
             'sc', 'syc', '690', 'sudan', 'sd', 'sdn', '729', 'sweden', 'se', 'swe', '752', 'singapore', 'sg', 'sgp',
             '702', 'saint helena', 'sh', 'shn', '654', 'slovenia', 'si', 'svn', '705', 'svalbard and jan mayen', 'sj',
             'sjm', '744', 'slovakia', 'sk', 'svk', '703', 'sierra leone', 'sl', 'sle', '694', 'san marino', 'sm',
             'smr', '674', 'senegal', 'sn', 'sen', '686', 'somalia', 'so', 'som', '706', 'suriname', 'sr', 'sur', '740',
             'south sudan', 'ss', 'ssd', '728', 'sao tome and principe', 'st', 'stp', '678', 'el salvador', 'sv', 'slv',
             '222', 'sint maarten', 'sx', 'sxm', '534', 'syrian arab republic', 'sy', 'syr', '760', 'eswatini', 'sz',
             'swz', '748', 'the turks and caicos islands', 'tc', 'tca', '796', 'chad', 'td', 'tcd', '148',
             'the french southern territories', 'tf', 'atf', '260', 'togo', 'tg', 'tgo', '768', 'thailand', 'th', 'tha',
             '764', 'tajikistan', 'tj', 'tjk', '762', 'tokelau', 'tk', 'tkl', '772', 'timor-leste', 'tl', 'tls', '626',
             'turkmenistan', 'tm', 'tkm', '795', 'tunisia', 'tn', 'tun', '788', 'tonga', 'to', 'ton', '776', 'turkey',
             'tr', 'tur', '792', 'trinidad and tobago', 'tt', 'tto', '780', 'tuvalu', 'tv', 'tuv', '798', 'taiwan',
             'tw', 'twn', '158', 'united republic of tanzania', 'the united republic of tanzania', 'tanzania', 'tz',
             'tza', '834', 'ukraine', 'ua', 'ukr', '804', 'uganda', 'ug', 'uga', '800',
             'the united states minor outlying islands', 'um', 'umi', '581', 'the united states of america',
             'united states of america', 'america', 'united states', 'the united states', 'us', 'usa', '840', 'uruguay',
             'uy', 'ury', '858', 'uzbekistan', 'uz', 'uzb', '860', 'the holy see', 'va', 'vat', '336',
             'saint vincent and the grenadines', 'vc', 'vct', '670', 'venezuela', 've', 'ven', '862',
             'british virgin islands', 'vg', 'vgb', '092', 'us virgin islands', 'vi', 'vir', '850', 'viet nam',
             'vietnam', 'vn', 'vnm', '704', 'vanuatu', 'vu', 'vut', '548', 'wallis and futuna', 'wf', 'wlf', '876',
             'samoa', 'ws', 'wsm', '882', 'kosovo', 'xk', 'xxk', 'yemen', 'ye', 'yem', '887', 'mayotte', 'yt', 'myt',
             '175', 'south africa', 'za', 'zaf', '710', 'zambia', 'zm', 'zmb', '894', 'zimbabwe', 'zw', 'zwe', '716'
             )


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    await update.message.reply_text("I help you to get a country's flag, enter the country's name, UN Code, "
                                    "ISO Alpha-2 code,or ISO Alpha-3 code according https://www.iban.com/country-codes")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        """Get a country's flag via the country's name, UN Code, ISO Alpha-2 code,or ISO Alpha-3 code. 
           These codes can all be found at:
           https://www.iban.com/country-codes 
           This bot uses CountryFlagsAPI, bugs please report to @Phernando82"""
    )


async def flag(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    flag_searched = update.message.text
    flag_searched = flag_searched.lower()
    url = URL + flag_searched
    if flag_searched not in countries:
        await update.message.reply_text('Check that you have correctly typed the reference for the flag according '
                                        'https://www.iban.com/country-codes')
    else:
        await update.message.reply_text(url)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, flag))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
