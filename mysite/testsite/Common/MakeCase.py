#coding=utf-8

import time
import unittest
import sys
import os

filedir = os.getcwd()

sys.path.append(filedir + '/common')
sys.path.append(filedir + '/case')
sys.path.append(filedir + '/case/App')
sys.path.append(filedir + '/case/Collect')
sys.path.append(filedir + '/case/Comments')
sys.path.append(filedir + '/case/Flw')
sys.path.append(filedir + '/case/Friend')
sys.path.append(filedir + '/case/Gif')
sys.path.append(filedir + '/case/IM')
sys.path.append(filedir + '/case/Image')
sys.path.append(filedir + '/case/Log')
sys.path.append(filedir + '/case/MSG')
sys.path.append(filedir + '/case/Post')
sys.path.append(filedir + '/case/Reco')
sys.path.append(filedir + '/case/Search')
sys.path.append(filedir + '/case/Show')
sys.path.append(filedir + '/case/Tag')
sys.path.append(filedir + '/case/Topic')
sys.path.append(filedir + '/case/Uploads')
sys.path.append(filedir + '/case/User')
sys.path.append(filedir + '/case/Userrelate')
sys.path.append(filedir + '/case/Video')
sys.path.append(filedir + '/case/Trending')
sys.path.append(filedir + '/case/AD')


import config
import Reco_Feed
import Video_RecoAll,Video_LikeFeed,Video_LikeDetail,Video_ShareFeed,Video_ShareDetail,Video_DownloadFeed,Video_DownloadDetail,Video_ClickFeed,Video_ClickDetail,Video_Similar,Video_Recosimilar
import Video_Trending,Video_Love,Video_Poetryquotes,Video_Devotional,Video_Entertainment,Video_Mylife,Video_Wishes,Video_Lifestyle,Video_Comedy
import DPS_RecoAll,DPS_LikeDetail,DPS_ShareFeed,DPS_ShareDetail,DPS_DownloadDetail,DPS_ClickFeed,DPS_ClickDetail,DPS_similar_by_page,DPS_get_top_items_by_author
import Moment_RecoAll,Moment_LikeDetail,Moment_ShareDetail,Moment_DownloadDetail,Moment_ClickDetail
import Tag_RecoAll,Tag_Items,Tag_tag_association,Tag_video_items_by_page,Tag_picture_items_by_page,Tag_moment_items_by_page,Tag_tag_top_items,Tag_trend_tag_info
import Tag_featured_items_by_page,Tag_recent_items_by_page,Tag_trending_items_by_page
import Get_Video_By_Author,Get_Picture_By_Author,Get_Moment_By_Author
import Collect_Add,Collect_Info
import App_DeviceSignin,App_ConfAll,App_DeviceInstall,New_conf_get
import User_SetterSignin,User_SetterSignout,User_SetterUpdateUserInfo,User_SetterChkName,User_SetterUpdateAvatar,User_Conent,User_SyncStatus
import User_pre_login,User_sms_send_code,User_login_submit,User_get_item_by_author_post,User_user_like_post,User_upload_bgpicture
import Comment_Set,Comment_List,Comment_Del,Comment
import Upload_By_Meta_User,Upload_del_from_user,Upload_from_user,Upload
import Center_Notify,Msg_Tip,Msg_Pull
import Search_HotWord,Search_Trending,Search_Association,Search_Query,Search_trend_tag,Search_search
import Gif_RecoAll,Gif_Click,Gif_Like,Gif_Download,Gif_Share,Gif_Similar
import Nearby_Reco,Item_Info,Post_Like,Post_Click,Post_Download,Post_Share
import IM_get_server,IM_setting_get,IM_block_get,IM_block_set,IM_report_set
import Userrelate_UserInfo,Userrelate_UserFollowing,Userrelate_UserFollowers,Userrelate_UserAddFollow,Userrelate_UserRemoveFollow,User_CheckRegister,Friends
import Log_addlogs_public
import Flw_user_reco,Flw_new_content,Flw_timeline,Flw_mix_reco
import Topic_index_tags,Topic_home_id,Topic_member_admin_list,Topic_member_list,Topic_member_visit,Topic_rank_list
import Trending_tab_reco,Get_banner
import mediation_get

class TestWelike(unittest.TestCase):

    # ************************************************************ Trending ********************************************************************
    def Trending_tab_reco(self):
        Trending_tab_reco.case_Trending_tab_reco(self)

    def Get_banner(self):
        Get_banner.case_Get_banner(self)

    #*************************************************************** Video **********************************************************************
    def RecoFeed(self):
        Reco_Feed.case_RecoFeed(self)
        
    def VideoRecoAll(self):
        Video_RecoAll.case_VideoRecoAll(self)

    def VideoLikeFeed(self):
        Video_LikeFeed.case_VideoLikeFeed(self)
                
    def VideoLikeDetail(self):
        Video_LikeDetail.case_VideoLikeDetail(self)

    def VideoShareFeed(self):
        Video_ShareFeed.case_VideoShareFeed(self)

    def VideoShareDetail(self):
        Video_ShareDetail.case_VideoShareDetail(self)

    def VideoDownloadFeed(self):
        Video_DownloadFeed.case_VideoDownloadFeed(self)

    def VideoDownloadDetail(self):
        Video_DownloadDetail.case_VideoDownloadDetail(self)

    def VideoClickFeed(self):
        Video_ClickFeed.case_VideoClickFeed(self)

    def VideoClickDetail(self):
        Video_ClickDetail.case_VideoClickDetail(self)

    def VideoSimilar(self):
        Video_Similar.case_VideoSimilar(self)

    def VideoRecosimilar(self):
        Video_Recosimilar.case_Recosimilar(self)

    def VideoTrending(self):
        Video_Trending.case_VideoTrending(self)

    def VideoLove(self):
        Video_Love.case_VideoLove(self)

    def VideoPoetryquotes(self):
        Video_Poetryquotes.case_VideoPoetryquotes(self)

    def VideoDevotional(self):
        Video_Devotional.case_VideoDevotional(self)

    def VideoEntertainment(self):
        Video_Entertainment.case_VideoEntertainment(self)

    def VideoMylife(self):
        Video_Mylife.case_VideoMylife(self)

    def VideoWishes(self):
        Video_Wishes.case_VideoWishes(self)

    def VideoLifestyle(self):
        Video_Lifestyle.case_VideoLifestyle(self)

    def VideoComedy(self):
        Video_Comedy.case_VideoComedy(self)


    #**************************************************************** DPS ************************************************************************            
    def DPSRecoAll(self):
        DPS_RecoAll.case_DPSRecoAll(self)

    def DPSLikeDetail(self):
        DPS_LikeDetail.case_DPSLikeDetail(self)

    def DPSShareFeed(self):
        DPS_ShareFeed.case_DPSShareFeed(self)

    def DPSShareDetail(self):
        DPS_ShareDetail.case_DPSShareDetail(self)
    
    def DPSDownloadDetail(self):
        DPS_DownloadDetail.case_DPSDownloadDetail(self)

    def DPSClickFeed(self):
        DPS_ClickFeed.case_DPSClickFeed(self)

    def DPSClickDetail(self):
        DPS_ClickDetail.case_DPSClickDetail(self)

    def DPS_similar_by_page(self):
        DPS_similar_by_page.case_DPS_similar_by_page(self)

    def DPS_get_top_items_by_author(self):
        DPS_get_top_items_by_author.case_DPS_get_top_items_by_author(self)

    #**************************************************************** Moment ************************************************************************

    def MomentRecoAll(self):
        Moment_RecoAll.case_MomentRecoAll(self)   

    def MomentLikeDetail(self):
        Moment_LikeDetail.case_MomentLikeDetail(self)

    def MomentShareDetail(self):
        Moment_ShareDetail.case_MomentShareDetail(self)   

    def MomentDownloadDetail(self):
        Moment_DownloadDetail.case_MomentDownloadDetail(self)

    def MomentClickDetail(self):
        Moment_ClickDetail.case_MomentClickDetail(self)

    #***************************************************************** Tag ***************************************************************************

    def TagRecoAll(self):
        Tag_RecoAll.case_TagRecoAll(self)   

    def TagItems(self):
        Tag_Items.case_TagItems(self)

    def Tag_Association(self):
        Tag_tag_association.case_Tag_association(self)

    def Tag_tag_top_items(self):
        Tag_tag_top_items.case_Tag_tag_top_items(self)

    def Tag_trend_tag_info(self):
        Tag_trend_tag_info.case_Tag_trend_tag_info(self)

    def Video_Items_By_Page(self):
        Tag_video_items_by_page.case_video_items_by_page(self)

    def Picture_Items_By_Page(self):
        Tag_picture_items_by_page.case_picture_items_by_page(self)   

    def Moment_Items_By_Page(self):
        Tag_moment_items_by_page.case_moment_items_by_page(self)
        
    def Tag_trending_items_by_page(self):
        Tag_trending_items_by_page.case_Tag_trending_items_by_page(self)

    def Tag_recent_items_by_page(self):
        Tag_recent_items_by_page.case_Tag_recent_items_by_page(self)

    def Tag_featured_items_by_page(self):
        Tag_featured_items_by_page.case_Tag_featured_items_by_page(self)
    #*************************************************************** property *************************************************************************
        
    def GetVideoByAuthor(self):
        Get_Video_By_Author.case_GetVideoByAuthor(self)   

    def GetPictureByAuthor(self):
        Get_Picture_By_Author.case_GetPictureByAuthor(self)

    def GetMomentByAuthor(self):
        Get_Moment_By_Author.case_GetMomentByAuthor(self)

    #***************************************************************** Collect *************************************************************************

    def CollectAdd(self):
        Collect_Add.case_CollectAdd(self)

    def CollectInfo(self):
        Collect_Info.case_CollectInfo(self)

    #******************************************************************* App ****************************************************************************
    def AppDeviceSignin(self):
        App_DeviceSignin.case_AppDeviceSignin(self)
        
    def AppDeviceInstall(self):
        App_DeviceInstall.case_AppDeviceInstall(self)
        
    def AppConfAll(self):
        App_ConfAll.case_AppConfAll(self)

    def New_conf_get(self):
        New_conf_get.case_New_conf_get(self)
        
     
    #******************************************************************* User ***************************************************************************

    def UserSetterSignin(self):
        User_SetterSignin.case_UserSetterSignin(self)   

    def UserSetterSignout(self):
        User_SetterSignout.case_UserSetterSignout(self)

    def UserSetterUpdateUserInfo(self):
        User_SetterUpdateUserInfo.case_UserSetterUpdateUserInfo(self)
        
    def UserSetterChkName(self):
        User_SetterChkName.case_UserSetterChkName(self)

    def UserSetterUpdateAvatar(self):
        User_SetterUpdateAvatar.case_UserSetterUpdateAvatar(self)

    def UserConent(self):
        User_Conent.case_UserConent(self)

    def UserSyncStatus(self):
        User_SyncStatus.case_SyncStatus(self)
        
    def UserCheckRegister(self):
        User_CheckRegister.case_CheckRegister(self)

    def User_pre_login(self):
        User_pre_login.case_User_pre_login(self)

    def User_sms_send_code(self):
        User_sms_send_code.case_User_sms_send_code(self)

    def User_login_submit(self):
        User_login_submit.case_User_login_submit(self)

    def User_get_item_by_author_post(self):
        User_get_item_by_author_post.case_User_get_item_by_author_post(self)

    def User_user_like_post(self):
        User_user_like_post.case_User_user_like_post(self)

    def User_upload_bgpicture(self):
        User_upload_bgpicture.case_User_upload_bgpicture(self)
    #******************************************************************* comment ***************************************************************************

    def CommentSet(self):
        Comment_Set.case_CommentSet(self)

    def CommentList(self):
        Comment_List.case_CommentList(self)

    def CommentDel(self):
        Comment_Del.case_CommentDel(self)

    def Comment(self):
        Comment.case_Comment(self)


    #******************************************************************* media *****************************************************************************

    def UploadByMetaUser(self):
        Upload_By_Meta_User.case_UploadByMetaUser(self)

    def Upload_from_user(self):
        Upload_from_user.case_Upload_from_user(self)

    def Upload_del_from_user(self):
        Upload_del_from_user.case_Upload_del_from_user(self)

    # 上传功能case
    def Upload(self):
        Upload.case_Upload(self)

   #******************************************************************* Userrelate *************************************************************************

    def UserrelateUserInfo(self):
        Userrelate_UserInfo.case_UserInfo(self)

    def UserrelateUserFollowing(self):
        Userrelate_UserFollowing.case_UserFollowing(self)

    def UserrelateUserFollowers(self):
        Userrelate_UserFollowers.case_UserFollowers(self)

    def UserrelateUserAddFollow(self):
        Userrelate_UserInfo.case_UserInfo(self)

    def UserrelateUserRemoveFollow(self):
        Userrelate_UserRemoveFollow.case_UserRemoveFollow(self)

    def Friends(self):
        Friends.case_Friends(self)

   #**********************************************************************MsgCenter*****************************************************************************
    def Notify(self):
        Center_Notify.case_Notify(self)
        
    def Msg_Tip(self):
        Msg_Tip.case_MsgTip(self)
        
    def Msg_Pull(self):
        Msg_Pull.case_MsgPull(self)
        
   #**********************************************************************Search*****************************************************************************
    def SearchHotWord(self):
        Search_HotWord.case_SearchHotWord(self)

    def SearchTrending(self):
        Search_Trending.case_SearchTrending(self)

    def SearchAssociation(self):
        Search_Association.case_SearchAssociation(self)

    def SearchQuery(self):
        Search_Query.case_SearchQuery(self)

    def Search_trend_tag(self):
        Search_trend_tag.case_Search_trend_tag(self)

    def Search_search(self):
        Search_search.case_Search_search(self)
    #**********************************************************************Gif*****************************************************************************

    def GifRecoAll(self):
        Gif_RecoAll.case_GifRecoAll(self)

    def GifClick(self):
        Gif_Click.case_GifClick(self)

    def GifDownload(self):
        Gif_Download.case_GifDownload(self)

    def GifShare(self):
        Gif_Share.case_GifShare(self)

    def GifLike(self):
        Gif_Like.case_GifLike(self)

    def GifSimilar(self):
        Gif_Similar.case_GifSimilar(self)

    #**********************************************************************Nearby*****************************************************************************

    def Nearby_Reco(self):
        Nearby_Reco.case_NearbyReco(self)

    def Item_Info(self):
        Item_Info.case_ItemInfo(self)

    def Post_Like(self):
        Post_Like.case_PostLike(self)

    def Post_Click(self):
        Post_Click.case_PostClick(self)

    def Post_Download(self):
        Post_Download.case_PostDownload(self)

    def Post_Share(self):
        Post_Share.case_PostShare(self)
    #**********************************************************************IM Server**************************************************************************

    def IM_get_server(self):
        IM_get_server.case_IM_get_server(self)

    def IM_setting_get(self):
        IM_setting_get.case_IM_setting_get(self)

    def IM_block_get(self):
        IM_block_get.case_IM_block_get(self)

    def IM_block_set(self):
        IM_block_set.case_IM_block_set(self)

    def IM_report_set(self):
        IM_report_set.case_IM_report_set(self)

    # ********************************************************************** Log *****************************************************************************

    def Log_addlogs_public(self):
        Log_addlogs_public.case_Log_addlogs_public(self)

    # ********************************************************************** Flw *****************************************************************************

    def Flw_user_reco(self):
        Flw_user_reco.case_Flw_user_reco(self)

    def Flw_timeline(self):
        Flw_timeline.case_Flw_timeline(self)

    def Flw_new_content(self):
        Flw_new_content.case_Flw_new_content(self)

    def Flw_mix_reco(self):
        Flw_mix_reco.case_Flw_mix_reco(self)

    # ********************************************************************** Topic *****************************************************************************

    def Topic_index_tags(self):
        Topic_index_tags.case_Topic_index_tags(self)

    def Topic_home_id(self):
        Topic_home_id.case_Topic_home_id(self)

    def Topic_member_admin_list(self):
        Topic_member_admin_list.case_Topic_member_admin_list(self)

    def Topic_member_list(self):
        Topic_member_list.case_Topic_member_list(self)

    def Topic_member_visit(self):
        Topic_member_visit.case_Topic_member_visit(self)

    def Topic_rank_list(self):
        Topic_rank_list.case_Topic_rank_list(self)

    # ********************************************************************** AD *****************************************************************************

    def mediation_get(self):
        mediation_get.case_mediation_get(self)