;!function(){try { var e="undefined"!=typeof globalThis?globalThis:"undefined"!=typeof global?global:"undefined"!=typeof window?window:"undefined"!=typeof self?self:{},n=(new e.Error).stack;n&&((e._debugIds|| (e._debugIds={}))[n]="25504548-7c30-d5af-a7ea-531b71c2e50b")}catch(e){}}();
(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,767204,e=>{"use strict";e.i(497338),e.i(328992),e.i(973521),e.s([])},70226,e=>{"use strict";let t,i="u">typeof crypto&&crypto.randomUUID&&crypto.randomUUID.bind(crypto),r=new Uint8Array(16),n=[];for(let e=0;e<256;++e)n.push((e+256).toString(16).slice(1));e.s(["v4",0,function(e,s,o){if(i&&!s&&!e)return i();let a=(e=e||{}).random??e.rng?.()??function(){if(!t){if("u"<typeof crypto||!crypto.getRandomValues)throw Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");t=crypto.getRandomValues.bind(crypto)}return t(r)}();if(a.length<16)throw Error("Random bytes length must be >= 16");if(a[6]=15&a[6]|64,a[8]=63&a[8]|128,s){if((o=o||0)<0||o+16>s.length)throw RangeError(`UUID byte range ${o}:${o+15} is out of buffer bounds`);for(let e=0;e<16;++e)s[o+e]=a[e];return s}return function(e,t=0){return(n[e[t+0]]+n[e[t+1]]+n[e[t+2]]+n[e[t+3]]+"-"+n[e[t+4]]+n[e[t+5]]+"-"+n[e[t+6]]+n[e[t+7]]+"-"+n[e[t+8]]+n[e[t+9]]+"-"+n[e[t+10]]+n[e[t+11]]+n[e[t+12]]+n[e[t+13]]+n[e[t+14]]+n[e[t+15]]).toLowerCase()}(a)}],70226)},927561,e=>{"use strict";var t=e.i(572646),i=e.i(920635),r=Object.defineProperty,n=(e,t,i)=>{let n;return(n="symbol"!=typeof t?t+"":t)in e?r(e,n,{enumerable:!0,configurable:!0,writable:!0,value:i}):e[n]=i};class s{constructor(e){n(this,"_libLoaded",!1),n(this,"_loadPromise",null),n(this,"state","init"),this.console=e}isBrowserSupported(){try{return"u">typeof window.shaka&&window.shaka.Player.isBrowserSupported()}catch(e){return this.console.log("[isBrowserSupported] Error checking Shaka support:",e),!1}}async loadLibrary(){return!!this._libLoaded||(this._loadPromise||(this._loadPromise=this._loadShakaLibrary()),this._loadPromise)}async createPlayer(){try{if(this.state="loading",!await this.loadLibrary())return{success:!1,error:{code:3002,message:"Failed to load Shaka Player library",severity:"fatal",recoverable:!1}};if(!this.isBrowserSupported())return{success:!1,error:{code:3001,message:"Browser is not supported for Shaka Player",severity:"fatal",recoverable:!1}};let e=new window.shaka.Player;return this.state="ready",this.console.log("[ShakaPlayerLoader] Player created successfully"),{success:!0,player:e}}catch(e){return this.state="error",this.console.log("[ShakaPlayerLoader] Failed to create player:",e),{success:!1,error:{code:3003,message:`Failed to initialize Shaka Player: ${e.message}`,severity:"fatal",recoverable:!1,details:{error:e}}}}}handleShakaError(e){let t=e.detail||e,i=this._mapShakaErrorSeverity(t.severity),r=this._isShakaErrorRecoverable(t.code);return{code:t.code||4e3,message:t.message||"Shaka Player error",severity:i,recoverable:r,details:{shakaError:t,category:t.category,data:t.data}}}async disposePlayer(e){try{this.console.log("[ShakaPlayerLoader] Disposing player"),await e.destroy()}catch(e){this.console.log("[ShakaPlayerLoader] Error during player disposal:",e)}}async _loadShakaLibrary(){try{if(window.shaka)return this._libLoaded=!0,!0;let t=await e.A(92054);return window.shaka=t.default||t,this.console.log("[ShakaPlayerLoader] Installing polyfills"),window.shaka.polyfill.installAll(),this._libLoaded=!0,this.console.log("[ShakaPlayerLoader] Library loaded successfully"),!0}catch(e){return this.console.error("ohnoz"),this.console.log("[ShakaPlayerLoader] Failed to load library:",e),!1}}_mapShakaErrorSeverity(e){switch(e){case 1:return"warning";case 2:return"error";default:return"fatal"}}_isShakaErrorRecoverable(e){return e>=1e3&&e<2e3||e>=3e3&&e<4e3&&[3014,3015,3016].includes(e)}}let o={},a=(0,i.createContext)(null),u=({children:e,autoInit:r,shakaConfig:n,showLogs:u})=>{let l={autoInit:r??!0,shakaConfig:n??o,showLogs:u??!1},c=(({showLogs:e})=>(0,i.useMemo)(()=>({debug:(...t)=>{e&&console.debug(...t)},log:(...t)=>{e&&(console.groupCollapsed(...t),console.trace(...t),console.groupEnd())},warn:(...e)=>{console.warn(...e)},error:(...e)=>{console.error(...e)}}),[e]))({showLogs:l.showLogs}),d=(0,i.useRef)(new Map).current,p=(0,i.useMemo)(()=>new s(c),[c]),y=(0,i.useCallback)(e=>{p.createPlayer().then(t=>{t.success?e.setShakaPlayer(t.player,l.shakaConfig):e.setError("Failed to initialize Shaka player",t.error)}).catch(t=>{e.setError("Failed to load Shaka player",t)})},[l.shakaConfig,p]),h=(0,i.useCallback)((e,t)=>{y(t),d.set(e,t)},[y,d]),b=(0,i.useCallback)(()=>{"init"===p.state?(c.log("[MediaPlayerProvider] auto init shaka library"),p.loadLibrary()):c.log("[MediaPlayerProvider] Shaka player already initialized",p.state)},[c,p]);(0,i.useEffect)(()=>{l.autoInit?(c.log("[MediaPlayerProvider] Auto initialize shaka"),b()):c.log("[MediaPlayerProvider] Auto initialize is disabled")},[]),(0,i.useEffect)(()=>()=>{d.forEach(e=>{e.dispose()}),d.clear()},[d]);let P={console:c,registerStore:h,shakaLoader:p,shakaConfig:l.shakaConfig,stores:d};return(0,t.jsx)(a.Provider,{value:P,children:e})},l=()=>{let e=i.default.useContext(a);if(!e)throw Error("useMediaPlayerContext must be used within a MediaPlayerProvider");return e};e.s(["MediaPlayerContext",()=>a,"MediaPlayerProvider",()=>u,"useMediaPlayerContext",()=>l],927561)},267553,976372,223621,142655,e=>{"use strict";let t,i,r,n,s,o,a,u,l;var c=e.i(572646),d=e.i(920635);e.i(590499);var p=e.i(424456),y=e.i(196074),h=e.i(186710);let b=(0,e.i(301467).createFetcher)({});var P=((t=P||{}).Aud="AUD",t.Brl="BRL",t.Cad="CAD",t.Clp="CLP",t.Cop="COP",t.Dkk="DKK",t.Egp="EGP",t.Eur="EUR",t.Gbp="GBP",t.Idr="IDR",t.Ils="ILS",t.Inr="INR",t.Jpy="JPY",t.Krw="KRW",t.Mxn="MXN",t.Myr="MYR",t.Ngn="NGN",t.Nok="NOK",t.Pen="PEN",t.Php="PHP",t.Pln="PLN",t.Ron="RON",t.Rub="RUB",t.Sgd="SGD",t.Thb="THB",t.Try="TRY",t.Twd="TWD",t.Usd="USD",t.Vnd="VND",t.Zar="ZAR",t),v=((i=v||{}).Day="DAY",i.Month="MONTH",i.Week="WEEK",i.Year="YEAR",i),S=((r=S||{}).GeneralCoupon="GENERAL_COUPON",r.InstructorCoupon="INSTRUCTOR_COUPON",r.UdemyCoupon="UDEMY_COUPON",r),m=((n=m||{}).PlanPriceDiscount="PLAN_PRICE_DISCOUNT",n.TrialDiscount="TRIAL_DISCOUNT",n),g=((s=g||{}).Fixed="FIXED",s.Percentage="PERCENTAGE",s),f=((o=f||{}).Consumersubscription="CONSUMERSUBSCRIPTION",o.ConsumersubscriptionPlusGrowWithGoogle="CONSUMERSUBSCRIPTION_PLUS_GROW_WITH_GOOGLE",o.ConsumersubscriptionValuePlan="CONSUMERSUBSCRIPTION_VALUE_PLAN",o.Enterprise="ENTERPRISE",o.Enterprisepro="ENTERPRISEPRO",o.EnterpriseAiGrowth="ENTERPRISE_AI_GROWTH",o.EnterpriseAiReadiness="ENTERPRISE_AI_READINESS",o.EnterpriseBase="ENTERPRISE_BASE",o.GrowWithGoogle="GROW_WITH_GOOGLE",o.Team="TEAM",o.Udemypro="UDEMYPRO",o),C=((a=C||{}).Active="ACTIVE",a.Canceled="CANCELED",a.Expired="EXPIRED",a.Future="FUTURE",a.Retired="RETIRED",a.Trial="TRIAL",a);let E=`
    fragment SubscriptionPlanFields on SubscriptionPlan {
  id
  productType
  urlLearnMore
  urlExpressCheckout
  urlTermsOfUse
  contentCollections {
    id
    stats {
      numberOfCourses
      courseAvgRating
      numberOfInstructors
      numberOfPracticeExercises
    }
  }
  priceOptions(
    licenseCount: $licenseCount
    marketingURL: $marketingURL
    couponCode: $couponCode
    excludeTrialOffers: $excludeTrialOffers
  ) {
    ... on MonthlySubscriptionPlanPricingOption {
      id
      listPrice {
        amount
        currency
      }
      price {
        list
        discount
        monthly
        annualSavings
        discountMonthly
        discountAnnualSavings
        currency
      }
      discountTrial {
        dateInterval {
          type
          count
        }
      }
      discount {
        appliedDiscounts {
          code
          discountType
          isRemovable
          sourceType
          data {
            ... on SubscriptionPlanTrialDiscountData {
              days
            }
            ... on SubscriptionPlanPriceDiscountData {
              type
              value
              interval {
                start
                end
                type
                duration
              }
            }
          }
        }
      }
      renewalInterval {
        type
        count
      }
      trial {
        dateInterval {
          type
          count
        }
      }
      licenseContext {
        unitPrice {
          amount
          currency
        }
        licenseCount
        defaultLicenseCount
        minimumLicenseCount
        maximumLicenseCount
      }
    }
    ... on AnnualSubscriptionPlanPricingOption {
      id
      listPrice {
        amount
        currency
      }
      price {
        list
        discount
        monthly
        annualSavings
        discountMonthly
        discountAnnualSavings
        currency
      }
      discountTrial {
        dateInterval {
          type
          count
        }
      }
      discount {
        appliedDiscounts {
          code
          discountType
          isRemovable
          sourceType
          data {
            ... on SubscriptionPlanTrialDiscountData {
              days
            }
            ... on SubscriptionPlanPriceDiscountData {
              type
              value
              interval {
                start
                end
                type
                duration
              }
            }
          }
        }
      }
      annualSavings {
        amount
        currency
      }
      monthlyPrice {
        amount
        currency
      }
      renewalInterval {
        type
        count
      }
      trial {
        dateInterval {
          type
          count
        }
      }
      licenseContext {
        unitPrice {
          amount
          currency
        }
        licenseCount
        defaultLicenseCount
        minimumLicenseCount
        maximumLicenseCount
      }
    }
    ... on WeeklySubscriptionPlanPricingOption {
      id
      listPrice {
        amount
        currency
      }
      price {
        list
        discount
        monthly
        annualSavings
        discountMonthly
        discountAnnualSavings
        currency
      }
      discountTrial {
        dateInterval {
          type
          count
        }
      }
      discount {
        appliedDiscounts {
          code
          discountType
          isRemovable
          sourceType
          data {
            ... on SubscriptionPlanTrialDiscountData {
              days
            }
            ... on SubscriptionPlanPriceDiscountData {
              type
              value
              interval {
                start
                end
                type
                duration
              }
            }
          }
        }
      }
      renewalInterval {
        type
        count
      }
      trial {
        dateInterval {
          type
          count
        }
      }
      licenseContext {
        unitPrice {
          amount
          currency
        }
        licenseCount
        defaultLicenseCount
        minimumLicenseCount
        maximumLicenseCount
      }
    }
    ... on DailySubscriptionPlanPricingOption {
      id
      listPrice {
        amount
        currency
      }
      price {
        list
        discount
        monthly
        annualSavings
        discountMonthly
        discountAnnualSavings
        currency
      }
      discountTrial {
        dateInterval {
          type
          count
        }
      }
      discount {
        appliedDiscounts {
          code
          discountType
          isRemovable
          sourceType
          data {
            ... on SubscriptionPlanTrialDiscountData {
              days
            }
            ... on SubscriptionPlanPriceDiscountData {
              type
              value
              interval {
                start
                end
                type
                duration
              }
            }
          }
        }
      }
      renewalInterval {
        type
        count
      }
      trial {
        dateInterval {
          type
          count
        }
      }
      licenseContext {
        unitPrice {
          amount
          currency
        }
        licenseCount
        defaultLicenseCount
        minimumLicenseCount
        maximumLicenseCount
      }
    }
  }
}
    `,R=`
    query CourseSubscriptions($landingURL: URL!, $licenseCount: Int, $marketingURL: URL, $couponCode: String, $excludeTrialOffers: Boolean) {
  courseByLandingURL(landingURL: $landingURL) {
    subscriptionInfo {
      inSubscriptions {
        id
        productType
      }
      availableInSubscriptions {
        ...SubscriptionPlanFields
      }
      availableInSubscriptionFamily {
        ...SubscriptionPlanFields
      }
    }
  }
}
    ${E}`,O=(e,t)=>(0,h.useQuery)({queryKey:["CourseSubscriptions",e],queryFn:b(R,e),...t});O.getKey=e=>["CourseSubscriptions",e],O.fetcher=(e,t)=>b(R,e,t);let T=`
    query GetAllAvailableConsumerSubscriptionPlans($licenseCount: Int, $marketingURL: URL, $couponCode: String, $excludeTrialOffers: Boolean) {
  subscriptionPlanUpgradesByProductFamily(productFamily: CONSUMER) {
    ...SubscriptionPlanFields
  }
}
    ${E}`,D=(e,t)=>(0,h.useQuery)({queryKey:void 0===e?["GetAllAvailableConsumerSubscriptionPlans"]:["GetAllAvailableConsumerSubscriptionPlans",e],queryFn:b(T,e),...t});D.getKey=e=>void 0===e?["GetAllAvailableConsumerSubscriptionPlans"]:["GetAllAvailableConsumerSubscriptionPlans",e],D.fetcher=(e,t)=>b(T,e,t);let I=`
    query SubscriptionPlans($filters: SubscriptionPlanFilters, $licenseCount: Int, $marketingURL: URL, $couponCode: String, $excludeTrialOffers: Boolean) {
  subscriptionPlans(filters: $filters) {
    ...SubscriptionPlanFields
  }
  currentSubscriptionEnrollment {
    id
    status
    subscribedPlan {
      id
      productType
    }
  }
}
    ${E}`,L=(e,t)=>(0,h.useQuery)({queryKey:void 0===e?["SubscriptionPlans"]:["SubscriptionPlans",e],queryFn:b(I,e),...t});L.getKey=e=>void 0===e?["SubscriptionPlans"]:["SubscriptionPlans",e],L.fetcher=(e,t)=>b(I,e,t),e.s(["CurrencyCode",()=>P,"DateIntervalType",()=>v,"SubscriptionPlanProductType",()=>f,"SubscriptionStatus",()=>C,"useCourseSubscriptionsQuery",()=>O,"useGetAllAvailableConsumerSubscriptionPlansQuery",()=>D,"useSubscriptionPlansQuery",()=>L],976372);let w={isLoading:!0},U={isSubscriber:!0,isLoading:!1};var M=((u=M||{}).Consumersubscription="CONSUMERSUBSCRIPTION",u.ConsumersubscriptionValuePlan="CONSUMERSUBSCRIPTION_VALUE_PLAN",u.GrowWithGoogle="GROW_WITH_GOOGLE",u.ConsumersubscriptionPlusGrowWithGoogle="CONSUMERSUBSCRIPTION_PLUS_GROW_WITH_GOOGLE",u.Team="TEAM",u),A=((l=A||{}).Percentage="PERCENTAGE",l.Fixed="FIXED",l);e.s(["SubscriptionPlanIsLoading",()=>w,"SubscriptionPlanPriceDiscountType",()=>A,"SubscriptionPlanProductType",()=>M,"SubscriptionPlanSubscribedState",()=>U],223621);var k=Object.defineProperty,N=(e,t,i)=>{let r;return(r="symbol"!=typeof t?t+"":t)in e?k(e,r,{enumerable:!0,configurable:!0,writable:!0,value:i}):e[r]=i};class G{constructor(e){N(this,"getPlanPriceOptionDiscount",(e,t)=>{var i;if(!this.getAppliedDiscount(e))return;let r=null==(i=null==e?void 0:e.price)?void 0:i.currency,n=this.getSubscriptionDiscountPrice(e),s=this.getSubscriptionNonDiscountPrice(e),o=this.getSubscriptionDiscountMonthlyPrice(e),a=this.getSubscriptionNonDiscountMonthlyPrice(e);return{subscriptionDiscountTrial:(null==e?void 0:e.discountTrial)||void 0,subscriptionNonDiscountPrice:String(s||""),subscriptionDiscountInterval:this.getSubscriptionDiscountDuration(e),subscriptionDiscountPercent:String(this.getSubscriptionDiscountPercent(e)||""),subscriptionDiscountPrice:String(n||""),subscriptionDiscountMonthlyPrice:String(o||""),subscriptionNonDiscountMonthlyPrice:String(a||""),formattedSubscriptionDiscountPrice:t?t.formatCurrency(n??0,{currency:r??void 0}):String(n||""),formattedSubscriptionNonDiscountPrice:t?t.formatCurrency(s??0,{currency:r??void 0}):String(s||""),formattedSubscriptionDiscountMonthlyPrice:t?t.formatCurrency(o??0,{currency:r??void 0}):String(o||""),formattedSubscriptionNonDiscountMonthlyPrice:t?t.formatCurrency(a??0,{currency:r??void 0}):String(a||"")}}),N(this,"getSubscriptionDiscountPercent",e=>{let t=this.getAppliedDiscount(e);if(t&&"type"in t.data&&t.data.type===A.Percentage)return t.data.value}),N(this,"getSubscriptionDiscountPrice",e=>{var t;return null==(t=null==e?void 0:e.price)?void 0:t.discount}),N(this,"getSubscriptionDiscountMonthlyPrice",e=>{var t;return null==(t=null==e?void 0:e.price)?void 0:t.discountMonthly}),N(this,"getSubscriptionNonDiscountMonthlyPrice",e=>{var t;return null==(t=null==e?void 0:e.price)?void 0:t.monthly}),N(this,"getSubscriptionNonDiscountPrice",e=>{var t;return null==(t=null==e?void 0:e.price)?void 0:t.list}),N(this,"getSubscriptionDiscountDuration",e=>{let t=this.getAppliedDiscount(e);if(t&&"type"in t.data)return t.data.interval;if(t&&"days"in t.data){let e=t.data.days;return{type:v.Day,duration:e,start:0,end:e}}}),this.subscriptionPlan=e,this.subscriptionPlan=e}getLicenseContext(){var e,t;return null==(t=null==(e=this.subscriptionPlan)?void 0:e.priceOptions[0])?void 0:t.licenseContext}getPlanPriceOptions(){var e;return(null==(e=this.subscriptionPlan)?void 0:e.priceOptions)??[]}getPlanPriceOptionIds(){return this.getPlanPriceOptions().map(e=>e.id)}getContentCollectionIds(){var e;return(null==(e=this.subscriptionPlan.contentCollections)?void 0:e.map(e=>e.id))??[]}getPriceOption(e){return this.subscriptionPlan.priceOptions.find(t=>t.renewalInterval.type===e)}getTrialPeriodDays(e){var t;let i=null==e?void 0:e.trial;if((null==(t=null==i?void 0:i.dateInterval)?void 0:t.type)===v.Day)return i.dateInterval.count}getAppliedDiscount(e){var t;let i=null==e?void 0:e.discount;if((null==(t=null==i?void 0:i.appliedDiscounts)?void 0:t.length)>0)return i.appliedDiscounts[0]}getSelectedPriceOption(e){let t=this.getPriceOption(v.Year),i=this.getPriceOption(v.Month),r=this.getPlanPriceOptionDiscount(i,e),n=this.getPlanPriceOptionDiscount(t,e);return t&&i?r&&n?n.subscriptionDiscountMonthlyPrice<r.subscriptionDiscountMonthlyPrice?t:i:r||n?n?t:i:t:t??i}}class _{adaptBaseSubscriptionPlan(e,t){var i,r,n,s,o;let a=new G(e),u=a.getPriceOption(v.Year),l=a.getPriceOption(v.Month),c=null!=(i=null==u?void 0:u.annualSavings)&&i.amount?null==(r=null==u?void 0:u.annualSavings)?void 0:r.amount:void 0,d=c?t.formatCurrency(c,{currency:(null==(n=null==u?void 0:u.annualSavings)?void 0:n.currency)??void 0}):void 0,p=a.getPlanPriceOptions(),y=a.getPlanPriceOptionDiscount(l,t),h=a.getPlanPriceOptionDiscount(u,t),b=a.getSelectedPriceOption(t),P=a.getPlanPriceOptionDiscount(b,t),S=null==(s=null==b?void 0:b.price)?void 0:s.monthly,m=t.formatCurrency(S??0,{currency:(null==(o=null==b?void 0:b.price)?void 0:o.currency)??void 0}),g=t.formatCurrency((null==b?void 0:b.listPrice.amount)??0,{currency:(null==b?void 0:b.listPrice.currency)??void 0});return{annualPlanOption:u,defaultPlanOption:b,isAnnualPlanEnabled:!!u,formattedAnnualSavings:d,formattedListPrice:g,formattedMonthlyAmount:m,trialPeriodDays:a.getTrialPeriodDays(b),monthlyPlanOption:l,planPriceOptionIds:a.getPlanPriceOptionIds(),contentCollectionIds:a.getContentCollectionIds(),priceOption:e=>p.find(t=>t.renewalInterval.type===e),monthlyDiscount:y,annualDiscount:h,selectedDiscount:P,...e}}}class x extends _{adaptSubscriptionPlan(e,t){return{...this.adaptBaseSubscriptionPlan(e,t),productType:M.Consumersubscription}}}class B extends _{adaptSubscriptionPlan(e,t){return{...this.adaptBaseSubscriptionPlan(e,t),productType:M.ConsumersubscriptionValuePlan}}}class F extends _{adaptSubscriptionPlan(e,t){return{...this.adaptBaseSubscriptionPlan(e,t),productType:M.GrowWithGoogle}}}class W extends _{adaptSubscriptionPlan(e,t){return{...this.adaptBaseSubscriptionPlan(e,t),productType:M.ConsumersubscriptionPlusGrowWithGoogle}}}class ${adaptSubscriptionPlan(e,t){let i=new G(e),r=i.getContentCollectionIds(),n=i.getLicenseContext(),s=i.getPriceOption(v.Year),o=i.getPriceOption(v.Month),a=i.getSelectedPriceOption(t),u=(null==s?void 0:s.monthlyPrice)??(null==o?void 0:o.listPrice),l=t.formatCurrency((null==u?void 0:u.amount)??0,{currency:(null==u?void 0:u.currency)??void 0}),c=i.getPlanPriceOptionDiscount(s,t),d=i.getPlanPriceOptionDiscount(a,t);return{contentCollectionIds:r,maximumLicenseCount:null==n?void 0:n.maximumLicenseCount,minimumLicenseCount:null==n?void 0:n.minimumLicenseCount,licenseContext:n,formattedMonthlyAmount:l,planPriceOptionIds:i.getPlanPriceOptionIds(),trialPeriodDays:i.getTrialPeriodDays(a),priceOption:e=>i.getPriceOption(e),productType:M.Team,annualDiscount:c,selectedDiscount:d,...e}}}function Q(e){switch(e){case f.Consumersubscription:return new x;case f.ConsumersubscriptionValuePlan:return new B;case f.GrowWithGoogle:return new F;case f.ConsumersubscriptionPlusGrowWithGoogle:return new W;case f.Team:return new $;default:throw Error("Unsupported subscription plan product type")}}e.s(["adapterFor",()=>Q],142655),e.i(284008);var q=e.i(687155),K=e.i(309509),H=e.i(751331),V=e.i(387737);function j(e,t){return e.filter(e=>!t.includes(e))}var Y=class extends H.Subscribable{#e;#t;#i;#r;#n;#s;#o;#a;#u=[];constructor(e,t,i){super(),this.#e=e,this.#r=i,this.#i=[],this.#n=[],this.#t=[],this.setQueries(t)}onSubscribe(){1===this.listeners.size&&this.#n.forEach(e=>{e.subscribe(t=>{this.#l(e,t)})})}onUnsubscribe(){this.listeners.size||this.destroy()}destroy(){this.listeners=new Set,this.#n.forEach(e=>{e.destroy()})}setQueries(e,t){this.#i=e,this.#r=t,q.notifyManager.batch(()=>{let e=this.#n,t=this.#c(this.#i);this.#u=t,t.forEach(e=>e.observer.setOptions(e.defaultedQueryOptions));let i=t.map(e=>e.observer),r=i.map(e=>e.getCurrentResult()),n=i.some((t,i)=>t!==e[i]);e.length===i.length&&!n||(this.#n=i,this.#t=r,this.hasListeners()&&(j(e,i).forEach(e=>{e.destroy()}),j(i,e).forEach(e=>{e.subscribe(t=>{this.#l(e,t)})}),this.#d()))})}getCurrentResult(){return this.#t}getQueries(){return this.#n.map(e=>e.getCurrentQuery())}getObservers(){return this.#n}getOptimisticResult(e,t){let i=this.#c(e),r=i.map(e=>e.observer.getOptimisticResult(e.defaultedQueryOptions));return[r,e=>this.#p(e??r,t),()=>this.#y(r,i)]}#y(e,t){return t.map((i,r)=>{let n=e[r];return i.defaultedQueryOptions.notifyOnChangeProps?n:i.observer.trackResult(n,e=>{t.forEach(t=>{t.observer.trackProp(e)})})})}#p(e,t){return t?(this.#s&&this.#t===this.#a&&t===this.#o||(this.#o=t,this.#a=this.#t,this.#s=(0,V.replaceEqualDeep)(this.#s,t(e))),this.#s):e}#c(e){let t=new Map(this.#n.map(e=>[e.options.queryHash,e])),i=[];return e.forEach(e=>{let r=this.#e.defaultQueryOptions(e),n=t.get(r.queryHash);n?i.push({defaultedQueryOptions:r,observer:n}):i.push({defaultedQueryOptions:r,observer:new K.QueryObserver(this.#e,r)})}),i}#l(e,t){let i=this.#n.indexOf(e);if(-1!==i){var r;let e;this.#t=(r=this.#t,(e=r.slice(0))[i]=t,e),this.#d()}}#d(){if(this.hasListeners()){let e=this.#s,t=this.#y(this.#t,this.#u);e!==this.#p(t,this.#r?.combine)&&q.notifyManager.batch(()=>{this.listeners.forEach(e=>{e(this.#t)})})}}},z=e.i(185769),X=e.i(553792),J=e.i(934317),Z=e.i(728812),ee=e.i(525335),et=e.i(217202),ei=e.i(378007);f.Team,P.Usd,v.Year,v.Day,P.Usd;let er=new Set([f.Consumersubscription,f.ConsumersubscriptionValuePlan,f.GrowWithGoogle,f.ConsumersubscriptionPlusGrowWithGoogle]),en=[C.Trial,C.Active,C.Canceled,C.Retired];async function es(e,t){return(await D.fetcher(e)({url:t})).subscriptionPlanUpgradesByProductFamily}let eo=(0,d.createContext)({CONSUMERSUBSCRIPTION:void 0,CONSUMERSUBSCRIPTION_VALUE_PLAN:void 0,GROW_WITH_GOOGLE:void 0,CONSUMERSUBSCRIPTION_PLUS_GROW_WITH_GOOGLE:void 0,ENTERPRISE:void 0,ENTERPRISEPRO:void 0,TEAM:void 0,UDEMYPRO:void 0,ENTERPRISE_AI_GROWTH:void 0,ENTERPRISE_AI_READINESS:void 0,ENTERPRISE_BASE:void 0});function ea(e,t){let i={...e};return Object.entries(t).forEach(([e,t])=>{i[e]=t}),i}let eu=({subscriptionPlanQueryVariables:e,children:t})=>{let i,r,n=(0,d.useContext)(eo),s=(0,p.useDeepCompareMemo)(e),o=(i=(0,y.useFormatCurrency)(),r=function(e,t){let{user:i}=(0,ei.useCommonData)(),r={},n=Array.isArray(e)?e:e?[e]:[],s=n.filter(e=>{var t;return(null==(t=e.filters)?void 0:t.productType)&&er.has(e.filters.productType)}),o=n.filter(e=>{var t;return(null==(t=e.filters)?void 0:t.productType)&&!er.has(e.filters.productType)}),a=s.length>0?{queryKey:["consumerSubscriptionPlans",s[0]],queryFn:async()=>{var e;let r=function(e){if(!e)return;let{subscribedPlan:t,status:i}=e;if(t.productType&&en.includes(i))return{productType:t.productType,status:i}}(null==i?void 0:i.subscription),n=await es(s[0]||{},t),o={};for(let t of s){let i=null==(e=t.filters)?void 0:e.productType;if(i)if((null==r?void 0:r.productType)===i)o[i]={subscriptionPlan:{},isSubscriber:!0,isLoading:!1};else{let e=n.find(e=>e.productType===i);e&&(o[i]={subscriptionPlan:{...e,isLoading:!1,isSubscriber:!1},isSubscriber:!1,isLoading:!1})}}return o},enabled:!0}:null;return(function({queries:e,...t},i){let r=(0,z.useQueryClient)(void 0),n=(0,X.useIsRestoring)(),s=(0,J.useQueryErrorResetBoundary)(),o=d.useMemo(()=>e.map(e=>{let t=r.defaultQueryOptions(e);return t._optimisticResults=n?"isRestoring":"optimistic",t}),[e,r,n]);o.forEach(e=>{(0,ee.ensureSuspenseTimers)(e),(0,Z.ensurePreventErrorBoundaryRetry)(e,s)}),(0,Z.useClearResetErrorBoundary)(s);let[a]=d.useState(()=>new Y(r,o,t)),[u,l,c]=a.getOptimisticResult(o,t.combine),p=!n&&!1!==t.subscribed;d.useSyncExternalStore(d.useCallback(e=>p?a.subscribe(q.notifyManager.batchCalls(e)):et.noop,[a,p]),()=>a.getCurrentResult(),()=>a.getCurrentResult()),d.useEffect(()=>{a.setQueries(o,t)},[o,t,a]);let y=u.some((e,t)=>(0,ee.shouldSuspend)(o[t],e))?u.flatMap((e,t)=>{let i=o[t];if(i){let t=new K.QueryObserver(r,i);if((0,ee.shouldSuspend)(i,e))return(0,ee.fetchOptimistic)(i,t,s);(0,ee.willFetch)(e,n)&&(0,ee.fetchOptimistic)(i,t,s)}return[]}):[];if(y.length>0)throw Promise.all(y);let h=u.find((e,t)=>{let i=o[t];return i&&(0,Z.getHasError)({result:e,errorResetBoundary:s,throwOnError:i.throwOnError,query:r.getQueryCache().get(i.queryHash),suspense:i.suspense})});if(h?.error)throw h.error;return l(c())})({queries:[...a?[a]:[],...o.map((e,i)=>({queryKey:[`subscriptionPlans-${i}`,e],queryFn:async()=>{var i,r,n;let s=await L.fetcher(e)({url:t}),o=null==(i=s.subscriptionPlans)?void 0:i[0],a=s.currentSubscriptionEnrollment,u=null==(r=e.filters)?void 0:r.productType;if(!u)return{};let l=a&&en.includes(a.status)&&(null==(n=a.subscribedPlan)?void 0:n.productType)===u;return o?{[u]:{subscriptionPlan:{...o,isLoading:!1,isSubscriber:!!l},isSubscriber:!!l,isLoading:!1}}:{[u]:{subscriptionPlan:{},isSubscriber:!!l,isLoading:!1}}},enabled:!0}))]}).forEach(e=>{e.data&&Object.entries(e.data).forEach(([e,t])=>{r[e]=t})}),r}(s,void 0),(0,d.useMemo)(()=>{let e={};return Object.entries(r).forEach(([t,r])=>{if(!r){e[t]=void 0;return}if(r.isSubscriber){e[t]={...U,productType:t};return}if(r.subscriptionPlan&&Object.keys(r.subscriptionPlan).length>0){let n=Q(t).adaptSubscriptionPlan(r.subscriptionPlan,i);e[t]=n}else r.isSubscriber?e[t]={isSubscriber:!0,isLoading:!1}:e[t]=void 0}),e},[r,i])),a=(0,d.useMemo)(()=>{let e={};return s.forEach(t=>{var i;let r=null==(i=t.filters)?void 0:i.productType,s=r&&void 0!==n[r];!r||r in o||s||(e[r]=w)}),ea(ea(n,e),o)},[o,n,s]);return(0,c.jsx)(eo.Provider,{value:a,children:t})};e.s(["ReactSubscriptionsContext",()=>eo,"SubscriptionPlansProvider",()=>eu],267553)},424842,e=>{e.v(t=>Promise.all(["static/chunks/7b901dc63c81ce1b.js"].map(t=>e.l(t))).then(()=>t(281593)))},882846,e=>{e.v(t=>Promise.all(["static/chunks/78a1ba55d1add6e9.js"].map(t=>e.l(t))).then(()=>t(80263)))},127140,e=>{e.v(e=>Promise.resolve().then(()=>e(301101)))},92054,e=>{e.v(t=>Promise.all(["static/chunks/fb8778723a98bb70.js"].map(t=>e.l(t))).then(()=>t(95869)))},209825,e=>{e.v(t=>Promise.all(["static/chunks/67c5548cc8e3d1a7.js"].map(t=>e.l(t))).then(()=>t(916609)))}]);

//# debugId=25504548-7c30-d5af-a7ea-531b71c2e50b
//# sourceMappingURL=f20a3c5e7237f62a.js.map